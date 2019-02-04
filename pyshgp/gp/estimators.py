"""The :mod:`estimator` module defines a ``PushEstimator`` class."""
import json

from pytypes import typechecked
from typing import Union, Tuple, Sequence

import numpy as np
import pandas as pd
from sklearn.utils.validation import check_is_fitted
# @TODO: Add more sklearn validation.

import pyshgp.gp.search as sr
import pyshgp.gp.selection as sl
import pyshgp.gp.variation as vr
from pyshgp.gp.evaluation import DatasetEvaluator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.interpreter import PushInterpreter, DEFAULT_INTERPRETER
from pyshgp.push.atoms import CodeBlock
from pyshgp.push.types import push_type_for_type
from pyshgp.utils import DiscreteProbDistrib, JSONable


class VariationStrategy(DiscreteProbDistrib):
    """A collection of VariationOperator and how frequently to use them."""

    @typechecked
    def add(self, op: vr.VariationOperator, p: float):
        """Add an element with a relative probability.

        Parameters
        ----------
        op : VariationOperator
            The VariationOperator to add to the variaiton strategy.
        p : float
            The probability of using the given operator relative to the other
            operators that have been added to the VariationStrategy.

        """
        super().add(op, p)


class SearchResult(JSONable):
    """The best program found by a search algorith and the types it outputs.

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
    variation_strategy : Union[VariationStrategy, str]
        A VariationStrategy or a name of a single variaiton operator to use when
        producing children.
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
    **kwargs
        Arbitrary keyword arguments. Examples of supported arguments are
        `use_epsilon_lexicase` (bool) when using Lexicase as the selector, and
        `tournament_size` (int) when using tournament selection.

    """

    def __init__(self,
                 search: Union[sr.SearchAlgorithm, str] = "GA",
                 spawner: Union[GeneSpawner, str] = "default",
                 selector: Union[sl.Selector, str] = "lexicase",
                 variation_strategy: Union[VariationStrategy, str] = "umad",
                 population_size: int = 300,
                 max_generations: int = 100,
                 initial_genome_size: Tuple[int, int] = (20, 100),
                 simplification_steps: int = 2000,
                 interpreter: PushInterpreter = "default",
                 **kwargs):
        self.search = search
        self.spawner = spawner
        self.selector = selector
        self.variation_strategy = variation_strategy
        self.population_size = population_size
        self.max_generations = max_generations
        self.initial_genome_size = initial_genome_size
        self.simplification_steps = simplification_steps

        if interpreter == "default":
            self.interpreter = DEFAULT_INTERPRETER
        else:
            self.interpreter = interpreter

        self.ext = kwargs

    # @TODO: Refactor so that new definitions don't need to be manually added.
    # Consider creating dicts of selectors, operators, etc. and looking up the
    # user given name to retreive the actual value.
    def _build_search_algo(self):
        if isinstance(self.spawner, GeneSpawner):
            self._spawner = self.spawner
        elif self.spawner == "default":
            self._spawner = GeneSpawner(
                instruction_set=self.interpreter.instruction_set,
                literals=[],
                erc_generators=[]
            )
        else:
            raise ValueError("Bad spawner: {}".format(self.spawner))

        if isinstance(self.selector, sl.Selector):
            self._selector = self.selector
        elif self.selector == "lexicase":
            self._selector = sl.Lexicase(self.ext.get("use_epsilon_lexicase", True))
        elif self.selector == "tournament":
            self._selector = sl.Tournament(self.ext.get("tournament_size", 7))
        elif self.selector == "roulette":
            self._selector = sl.FitnessProportionate()
        elif self.selector == "elite":
            self._selector = sl.Elite()
        else:
            raise ValueError("Bad selector: {}".format(self.selector))

        if isinstance(self.variation_strategy, VariationStrategy):
            self._variation_strategy = self.variation_strategy
        elif self.variation_strategy == "umad":
            self._variation_strategy = vr.SIZE_NEUTRAL_UMAD
        else:
            raise ValueError("Bad variation strategy: {}".format(self.variation_strategy))

        search_config = sr.SearchConfiguration(
            spawning=self._spawner, evaluator=self.evaluator, selection=self._selector,
            variation=self._variation_strategy, population_size=self.population_size,
            max_generations=self.max_generations,
            initial_genome_size=self.initial_genome_size,
            simplification_steps=self.simplification_steps
        )

        if isinstance(self.search, sr.SearchAlgorithm):
            self._search = self.search
        elif self.search == "GA":
            self._search = sr.GeneticAlgorithm(search_config)
        elif self.search == "SA":
            self._search = sr.SimulatedAnnealing(search_config)
        else:
            raise ValueError("Bad search algorithm: {}".format(self.search))

    def fit(self, X, y, verbose: bool = False):
        """Run the search algorithm to synthesize a push program.

        Parameters
        ----------
        X : pandas dataframe of shape = [n_samples, n_features]
            The training input samples.
        y : list, array-like, or pandas dataframe.
            The target values (class labels in classification, real numbers in
            regression). Shape = [n_samples] or [n_samples, n_outputs]
        verbose : bool, optional
            Indicates if verbose printing should be used during searching.
            Default is False.

        """
        if isinstance(X, (pd.DataFrame, np.ndarray)):
            if len(X.shape) > 1:
                arity = X.shape[1]
            else:
                arity = 1
        elif isinstance(y, (pd.Series, list)):
            # @TODO: How does sklearn do data shape validation?
            try:
                arity = len(X[0])
            except TypeError:
                arity = 1
        else:
            arity = 1
        self.interpreter.instruction_set.register_n_inputs(arity)

        if isinstance(y, pd.DataFrame):
            y_types = list(y.dtypes)
        elif isinstance(y, pd.Series):
            y_types = [y.dtype]
        elif isinstance(y, np.ndarray):
            if len(y.shape) > 1:
                y_types = [y.dtype] * y.shape[1]
            else:
                y_types = [y.dtype]
        elif isinstance(y[0], list):
            # @TODO: Find better way to detect type than check the first element.
            y_types = [type(_) for _ in y[0]]
        else:
            y_types = [type(y[0])]
        output_types = [push_type_for_type(t).name for t in y_types]

        self.evaluator = DatasetEvaluator(X, y, interpreter=self.interpreter)
        self._build_search_algo()
        best_seen = self._search.run(verbose)

        self._result = SearchResult(best_seen.program, output_types)

    def predict(self, X, verbose: bool = False):
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
            self.interpreter.run(self._result.program, inputs, self._result.output_types, verbose=verbose) for inputs in X
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
        self.evaluator = DatasetEvaluator(X, y)
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
