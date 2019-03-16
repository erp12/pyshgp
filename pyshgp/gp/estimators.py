"""The :mod:`estimator` module defines a ``PushEstimator`` class."""
import json
from typing import Union, Tuple, Sequence

import pyshgp.gp.search as sr
import pyshgp.gp.selection as sl
import pyshgp.gp.variation as vr
from pyshgp.gp.evaluation import DatasetEvaluator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.interpreter import PushInterpreter, DEFAULT_INTERPRETER
from pyshgp.push.atoms import CodeBlock
from pyshgp.push.types import push_type_for_type
from pyshgp.utils import JSONable, list_rindex
from pyshgp.validation import check_is_fitted, check_X_y
from pyshgp.monitoring import DEFAULT_VERBOSITY_LEVELS


class SearchResult(JSONable):
    """The best program found by a search algorithm and the types it outputs.

    Parameters
    ----------
    program : CodeBlock
        The Push program found by a SearchAlgorithm.
    output_types : Sequence[str]
        The types output by the program.

    Attributes
    ----------
    program : CodeBlock
        The Push program found by a SearchAlgorithm.
    output_types : Sequence[str]
        The types output by the program.

    """

    def __init__(self, program: CodeBlock, output_types: Sequence[str]):
        self.program = program
        self.output_types = output_types

    @classmethod
    def from_json_str(cls, json_str: str, instruction_set: InstructionSet):
        """Create a PushSolution from a JSON string."""
        solution_dict = json.loads(json_str)
        return cls(
            CodeBlock.from_json_str(
                json.dumps(solution_dict["program"], separators=(',', ':')),
                instruction_set
            ),
            solution_dict["output_types"]
        )

    @classmethod
    def from_json_file(cls, filepath: str, instruction_set: InstructionSet):
        """Create a PushSolution from a JSON string."""
        with open(filepath, "r") as f:
            return cls.from_json_str(f.read(), instruction_set)

    def jsonify(self):
        """Return the object as a JSON string."""
        return '{{"program":{p},"output_types":{o}}}'.format(
            p=self.program.to_json(),
            o="[" + ",".join(['"' + t + '"' for t in self.output_types]) + "]"
        )


class PushEstimator:
    """Simple estimator that synthesizes Push programs.

    Parameters
    ----------
    search : Union[SearchAlgorithm, str], optional
        The search algorithm, or its abbreviation, to use to when synthesizing
        Push programs.
    spawner : Union[GeneSpawner, str], optional
        The GeneSpawner to use when producing Genomes during initialization and
        variation. Default is all core intructions, no literals, and no ERC Generators.
    selector : Union[Selector, str], optional
        The selector, or name of selector, to use when selecting parents.
        The default is lexicase selection.
    variation_strategy : Union[VariationStrategy, dict, str]
        A VariationStrategy describing a collection of VariationOperators and how
        frequently to use them. If a dict is supplied, keys should be operator
        names and values should be the probability distirution. If a string is
        provided, the VariationOperators with that name will always be used.
    population_size : int, optional
        The number of individuals hold in the population each generation. Default
        is 300.
    max_generations : int, optional
        The number of generations to run the search algorithm. Default is 100.
    initial_genome_size : Tuple[int, int], optional
        The range of genome sizes to produce during initialization. Default is
        (20, 100)
    simplification_steps : int
        The number of simplification iterations to apply to the best Push program
        produced by the search algorithm.
    interpreter : PushInterpreter, optional
        The PushInterpreter to use when making predictions. Also holds the instruction
        set to use
    verbose : int, optional
        Indicates if verbose printing should be used during searching.
        Default is 0. Options are 0, 1, or 2.
    **kwargs
        Arbitrary keyword arguments. Examples of supported arguments are
        `epsilon` (bool or float) when using Lexicase as the selector, and
        `tournament_size` (int) when using tournament selection.

    """

    def __init__(self,
                 spawner: GeneSpawner,
                 search: str = "GA",
                 selector: Union[sl.Selector, str] = "lexicase",
                 variation_strategy: Union[vr.VariationStrategy, dict, str] = "umad",
                 population_size: int = 300,
                 max_generations: int = 100,
                 initial_genome_size: Tuple[int, int] = (20, 100),
                 simplification_steps: int = 2000,
                 last_str_from_stdout: bool = False,
                 interpreter: PushInterpreter = "default",
                 verbose: int = 0,
                 **kwargs):
        self._search_name = search
        self.spawner = spawner
        self.selector = selector
        self.variation_strategy = variation_strategy
        self.population_size = population_size
        self.max_generations = max_generations
        self.initial_genome_size = initial_genome_size
        self.simplification_steps = simplification_steps
        self.last_str_from_stdout = last_str_from_stdout
        self.verbose = verbose

        if interpreter == "default":
            self.interpreter = DEFAULT_INTERPRETER
        else:
            self.interpreter = interpreter

        self.ext = kwargs

    def _build_search_algo(self):
        if isinstance(self.variation_strategy, dict):
            var_strat = vr.VariationStrategy()
            for op_name, prob in self.variation_strategy.items():
                var_op = vr.get_variation_operator(op_name)
                if not isinstance(var_op, vr.VariationOperator):
                    var_op = self._build_component(var_op)
                var_strat.add(var_op, prob)
            self.variation_strategy = var_strat

        search_config = sr.SearchConfiguration(
            spawner=self.spawner,
            evaluator=self.evaluator,
            selection=self.selector,
            variation=self.variation_strategy,
            population_size=self.population_size,
            max_generations=self.max_generations,
            initial_genome_size=self.initial_genome_size,
            simplification_steps=self.simplification_steps,
            verbosity_config=DEFAULT_VERBOSITY_LEVELS[self.verbose]
        )
        self.search = sr.get_search_algo(self._search_name, config=search_config, **self.ext)

    def fit(self, X, y):
        """Run the search algorithm to synthesize a push program.

        Parameters
        ----------
        X : pandas dataframe of shape = [n_samples, n_features]
            The training input samples.
        y : list, array-like, or pandas dataframe.
            The target values (class labels in classification, real numbers in
            regression). Shape = [n_samples] or [n_samples, n_outputs]

        """
        X, y, arity, y_types = check_X_y(X, y)
        self.interpreter.instruction_set.register_n_inputs(arity)
        output_types = [push_type_for_type(t).name for t in y_types]
        if self.last_str_from_stdout:
            ndx = list_rindex(output_types, "str")
            if ndx is not None:
                output_types[ndx] = "stdout"
        self.evaluator = DatasetEvaluator(
            X, y,
            interpreter=self.interpreter,
            last_str_from_stdout=self.last_str_from_stdout,
            verbosity_config=DEFAULT_VERBOSITY_LEVELS[self.verbose]
        )
        self._build_search_algo()
        best_seen = self.search.run()
        self._result = SearchResult(best_seen.program, output_types)

    def predict(self, X):
        """Execute the synthesized push program on a dataset.

        Parameters
        ----------
        X : pandas dataframe of shape = [n_samples, n_features]
            The set of cases to predict.
        verbose : bool, optional
            Indicates if verbose printing should be used during searching.
            Default is False.

        Returns
        -------
        y_hat : pandas dataframe of shape = [n_samples, n_outputs]

        """
        check_is_fitted(self, "_result")
        return [
            self.interpreter.run(
                self._result.program,
                inputs,
                self._result.output_types,
                verbosity_config=self.search.config.verbosity_config
            ) for inputs in X
        ]

    def score(self, X, y):
        """Run the search algorithm to synthesize a push program.

        Parameters
        ----------
        X : pandas dataframe of shape = [n_samples, n_features]
            The training input samples.

        y : list, array-like, or pandas dataframe.
            The target values (class labels in classification, real numbers in
            regression). Shape = [n_samples] or [n_samples, n_outputs]

        """
        check_is_fitted(self, "_result")
        X, y, arity, y_types = check_X_y(X, y)
        self.evaluator = DatasetEvaluator(X, y, )
        return self.evaluator.evaluate(self._result.program)

    def save(self, filepath: str):
        """Load the found solution to a JSON file.

        Parameters
        ----------
        filepath
            Filepath to write the serialized search result to.

        """
        check_is_fitted(self, "_result")
        self._result.to_json(filepath)

    def load(self, filepath: str):
        """Load a found solution from a JSON file.

        Parameters
        ----------
        filepath
            Filepath to read the serialized search result from.

        """
        self._result = SearchResult.from_json_file(filepath, self.interpreter.instruction_set)
