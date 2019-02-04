"""The :mod:`search` module defines algorithms to search for Push programs."""
from abc import ABC, abstractmethod
from typing import Union, Tuple
from warnings import warn

from numpy.random import random
import math

from pyshgp.utils import DiscreteProbDistrib
from pyshgp.gp.evaluation import Evaluator
from pyshgp.gp.genome import GeneSpawner, GenomeSimplifier
from pyshgp.gp.individual import Individual
from pyshgp.gp.population import Population
from pyshgp.gp.selection import Selector, get_selector
from pyshgp.gp.variation import VariationOperator, get_variation_operator


# @TODO: Should SearchConfiguration be JSON serializable?
class SearchConfiguration:
    """Configuration of an search algorithm.

    Parameters
    ----------
    evaluator : Evaluator
        The Evaluator to use when evaluating individuals.
    spawning : Union[GeneSpawner, str], optional
        The GeneSpawner, or DiscreteProbDistrib of gene spawners to use when
        producing Genomes during initialization and variation.
    selection :Union[Selector, DiscreteProbDistrib, str], optional
        A Selector, or DiscreteProbDistrib of selectors, to use when selecting
        parents. The default is lexicase selection.
    variation : Union[VariationOperator, DiscreteProbDistrib, str], optional
        A VariationOperator, or DiscreteProbDistrib of VariationOperators, to
        use during variation. Default is SIZE_NEUTRAL_UMAD.
    population_size : int, optional
        The number of individuals hold in the population each generation. Default
        is 300.
    max_generations : int, optional
        The number of generations to run the search algorithm. Default is 100.
    error_threshold : float, optional
        If the search algorithm finds an Individual with a total error less
        than this values, stop searching. Default is 0.0.
    initial_genome_size : Tuple[int, int], optional
        The range of genome sizes to produce during initialization. Default is
        (20, 100)
    simplification_steps : int
        The number of simplification iterations to apply to the best Push program
        produced by the search algorithm.

    """

    def __init__(self,
                 evaluator: Evaluator,
                 spawning: Union[GeneSpawner, DiscreteProbDistrib],
                 selection: Union[Selector, DiscreteProbDistrib, str] = "lexicase",
                 variation: Union[VariationOperator, DiscreteProbDistrib, str] = "umad",
                 population_size: int = 500,
                 max_generations: int = 100,
                 error_threshold: float = 0.0,
                 initial_genome_size: Tuple[int, int] = (10, 50),
                 simplification_steps: int = 2000):
        self.evaluator = evaluator
        self.population_size = population_size
        self.max_generations = max_generations
        self.error_threshold = error_threshold
        self.initial_genome_size = initial_genome_size
        self.simplification_steps = simplification_steps

        if isinstance(spawning, DiscreteProbDistrib):
            self._spawning = spawning
        else:
            self._spawning = DiscreteProbDistrib().add(spawning, 1.0)

        if isinstance(selection, str):
            self._selection = DiscreteProbDistrib().add(get_selector(selection), 1.0)
        elif isinstance(selection, DiscreteProbDistrib):
            self._selection = selection
        else:
            self._selection = DiscreteProbDistrib().add(selection, 1.0)

        if variation == "umad":
            self._variation = DiscreteProbDistrib().add(get_variation_operator, 1.0)
        elif isinstance(variation, DiscreteProbDistrib):
            self._variation = variation
        else:
            self._variation = DiscreteProbDistrib().add(variation, 1.0)

    def get_spawner(self):
        """Return a GeneSpawner."""
        return self._spawning.sample()

    def get_selector(self):
        """Return a Selector."""
        return self._selection.sample()

    def get_variation_operator(self):
        """Return a VariationOperator."""
        return self._variation.sample()


class SearchAlgorithm(ABC):
    """Base class for all search algorithms.

    Parameters
    ----------
    config : SearchConfiguration
        The configuation of the search algorithm.

    Attributes
    ----------
    config : SearchConfiguration
        The configuation of the search algorithm.
    generation : int
        The current generation, or iteration, of the search.
    best_seen : Individual
        The best Individual, with respect to total error, seen so far.
    population : Population
        The current Population of individuals.

    """

    def __init__(self, config: SearchConfiguration):
        self.config = config
        self.generation = 0
        self.best_seen = None
        self.init_population()

    def init_population(self):
        """Initialize the population."""
        self.population = Population()
        for i in range(self.config.population_size):
            spawner = self.config.get_spawner()
            genome = spawner.spawn_genome(self.config.initial_genome_size)
            self.population.add(Individual(genome))

    @abstractmethod
    def step(self) -> bool:
        """Perform one generation (step) of the search. Return if should continue.

        The step method should assume an evaluated Population, and must only
        perform parent selection and variation (producing children). The step
        method should modify the search algorithms population in-place, or
        assign a new Population to the population attribute.

        """
        pass

    def _full_step(self, verbose: bool) -> bool:
        self.generation += 1
        self.population.evaluate(self.config.evaluator)

        best_this_gen = self.population.best()
        if self.best_seen is None or best_this_gen.total_error < self.best_seen.total_error:
            self.best_seen = best_this_gen
            if self.best_seen.total_error <= self.config.error_threshold:
                return False

        if verbose:
            stat_logs = []
            stat_logs.append("GENERATION: {g}".format(
                g=self.generation
            ))
            stat_logs.append("ERRORS: best={b}, median={m}, diversity={e_d}".format(
                b=self.population.best().total_error,
                m=self.population.median_error(),
                e_d=self.population.error_diversity()
            ))
            # stat_logs.append("Population: size={p_s}, genome_diversity={g_d}".format(
            #     p_s=len(self.population),
            #     g_d=self.population.genome_diversity()
            # ))
            print(" | ".join(stat_logs))

        self.step()
        return True

    def run(self, verbose: bool = False):
        """Run the algorithm until termination.

        Parameters
        ----------
        verbose : bool, optional
            Indicates if verbose printing should be used during searching.
            Default is False.

        """
        while self._full_step(verbose):
            if self.generation >= self.config.max_generations:
                break

        simplifier = GenomeSimplifier(self.config.evaluator, verbose)
        simp_genome, simp_error_vector = simplifier.simplify(
            self.best_seen.genome,
            self.best_seen.error_vector,
            self.config.simplification_steps
        )
        simplified_best = Individual(simp_genome)
        simplified_best.error_vector = simp_error_vector

        return simplified_best


class GeneticAlgorithm(SearchAlgorithm):
    """Genetic algorithm to synthesize Push programs.

    An initial Population of random Individuals is created. Each generation
    begins by evaluating all Individuals in the population. Then the current
    Popluation is replaced with children produced by selecting parents from
    the Population and applying VariationOperators to them.

    """

    def __init__(self, config: SearchConfiguration):
        super().__init__(config)

    def _make_child(self) -> Individual:
        op = self.config.get_variation_operator()
        selector = self.config.get_selector()
        parent_genomes = [p.genome for p in selector.select(self.population, n=op.num_parents)]
        child_genome = op.produce(parent_genomes, self.config.get_spawner())
        return Individual(child_genome)

    def step(self):
        """Perform one generation (step) of the genetic algorithm.

        The step method assumes an evaluated Population and performs parent
        selection and variation (producing children).

        """
        self.population = Population(
            [self._make_child() for _ in range(self.config.population_size)]
        )


class SimulatedAnnealing(SearchAlgorithm):
    """Algorithm to synthesize Push programs with Simulated Annealing.

    At each step (generation), the simulated annealing heuristic mutates the
    current Individual, and probabilistically decides between accepting or
    rejecting the child. If the child is accepted, it becomes the new current
    Individual.

    After each step, the simmulated annealing system cools its temperature.
    As the temperature lowers, the probability of accepting a child that does
    not have a lower total error than the current Individual decreases.

    """

    def __init__(self, config: SearchConfiguration):
        if not config.population_size == 1:
            warn("SimulatedAnnealing only supports a population size of 1. Config has been overwritten. ")
            config.population_size = 1

        for op in config._variation.elements:
            assert op.num_parents <= 1, "SimulatedAnnealing cannot take multiple parant variation operators."

        super().__init__(config)

    def _get_temp(self,):
        """Return the temperature."""
        return 1.0 - (self.generation / self.config.max_generations)

    def _acceptance(self, next_error):
        """Return probability of acceptance given an error."""
        current_error = self.population.best().total_error
        if next_error < current_error:
            return 1
        else:
            return math.exp(-(next_error - current_error) / self._get_temp())

    def step(self):
        """Perform one generation, or step, of the Simulated Annealing.

        The step method assumes an evaluated Population one Individual and
        produces a single candidate Individual. If the candidate individual
        passes the acceptance function, it becomes the Individual in the
        Population.

        """
        if self._get_temp() <= 0:
            return

        candidate = Individual(
            self.config.get_variation_operator().produce(
                [self.population.best().genome],
                self.config.get_spawner()
            )
        )
        candidate.error_vector = self.config.evaluator.evaluate(candidate.program)

        acceptance_probability = self._acceptance(candidate.total_error)
        if random() < acceptance_probability:
            self.population = Population().add(candidate)


# @TODO: class EvolutionaryStrategy(SearchAlgorithm):
#     ...


def get_search_algo(name: str) -> SearchAlgorithm:
    """Return the search algorithm class with the given name."""
    name_to_cls = {
        "GA": GeneticAlgorithm,
        "SA": SimulatedAnnealing,
        # "ES": EvolutionaryStrategy,
    }
    search_algo = name_to_cls.get(name, None)
    if search_algo is None:
        raise ValueError("No search algo '{nm}'. Supported names: {lst}.".format(
            nm=name,
            lst=list(name_to_cls.keys())
        ))
    return search_algo
