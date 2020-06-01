"""The :mod:`estimator` module defines a ``PushEstimator`` class."""
from typing import Union, Tuple

from pyshgp.gp.individual import Individual

import pyshgp.gp.search as sr
import pyshgp.gp.selection as sl
import pyshgp.gp.variation as vr
from pyshgp.gp.evaluation import DatasetEvaluator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.interpreter import PushInterpreter, DEFAULT_INTERPRETER
from pyshgp.push.config import PushConfig
from pyshgp.push.program import ProgramSignature
from pyshgp.tap import tap
from pyshgp.utils import list_rindex
from pyshgp.validation import check_is_fitted, check_X_y


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
    parallelism : Union[Int, bool], optional
        Set the number of processes to spawn for use when performing embarrassingly
        parallel tasks. If false, no processes will spawn and compuation will be
        serial. Default is true, which spawns one process per available cpu.
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
                 parallelism: Union[int, bool] = False,
                 push_config: PushConfig = "default",
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
        self.parallelism = parallelism
        self.verbose = verbose
        self.ext = kwargs

        # Initialize attributes that will be set later.
        self.evaluator = None
        self.signature = None
        self.search = None
        self.solution = None

        if interpreter == "default":
            self.interpreter = DEFAULT_INTERPRETER
        else:
            self.interpreter = interpreter

        if push_config == "default":
            self.push_config = PushConfig()
        else:
            self.push_config = push_config

    def _build_search_algo(self):
        if isinstance(self.variation_strategy, dict):
            var_strat = vr.VariationStrategy()
            for op_name, prob in self.variation_strategy.items():
                var_op = vr.get_variation_operator(op_name)
                var_strat.add(var_op, prob)
            self.variation_strategy = var_strat

        search_config = sr.SearchConfiguration(
            signature=self.signature,
            spawner=self.spawner,
            evaluator=self.evaluator,
            selection=self.selector,
            variation=self.variation_strategy,
            population_size=self.population_size,
            max_generations=self.max_generations,
            initial_genome_size=self.initial_genome_size,
            simplification_steps=self.simplification_steps,
            parallelism=self.parallelism,
            push_config=self.push_config,
            verbose=self.verbose
        )
        self.search = sr.get_search_algo(self._search_name, config=search_config, **self.ext)

    @tap
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
        output_types = [self.interpreter.type_library.push_type_for_type(t).name for t in y_types]
        if self.last_str_from_stdout:
            ndx = list_rindex(output_types, "str")
            if ndx is not None:
                output_types[ndx] = "stdout"
        self.signature = ProgramSignature(arity=arity, output_stacks=output_types, push_config=self.push_config)
        self.evaluator = DatasetEvaluator(X, y, interpreter=self.interpreter)
        self._build_search_algo()
        self.solution = self.search.run()

    def predict(self, X):
        """Execute the synthesized push program on a dataset.

        Parameters
        ----------
        X : pandas dataframe of shape = [n_samples, n_features]
            The set of cases to predict.

        Returns
        -------
        y_hat : pandas dataframe of shape = [n_samples, n_outputs]

        """
        check_is_fitted(self, "solution")
        return [
            self.interpreter.run(
                self.solution.program,
                inputs
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
        check_is_fitted(self, "solution")
        X, y, arity, y_types = check_X_y(X, y)
        self.evaluator = DatasetEvaluator(X, y, interpreter=self.interpreter)
        return self.evaluator.evaluate(self.solution.program)

    def save(self, filepath: str):
        """Load the found solution to a JSON file.

        Parameters
        ----------
        filepath
            Filepath to write the serialized search result to.

        """
        check_is_fitted(self, "solution")
        self.solution.save(filepath)

    def load(self, filepath: str):
        """Load a found solution from a JSON file.

        Parameters
        ----------
        filepath
            Filepath to read the serialized search result from.

        """
        self.solution = Individual.load(filepath)
