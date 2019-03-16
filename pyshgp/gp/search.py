"""The :mod:`search` module defines algorithms to search for Push programs."""
from abc import ABC, abstractmethod
from typing import Union, Tuple

import numpy as np
import math

from pyshgp.utils import DiscreteProbDistrib
from pyshgp.gp.evaluation import Evaluator
from pyshgp.gp.genome import GeneSpawner, GenomeSimplifier
from pyshgp.gp.individual import Individual
from pyshgp.gp.population import Population
from pyshgp.gp.selection import Selector, get_selector
from pyshgp.gp.variation import VariationOperator, get_variation_operator
from pyshgp.utils import instantiate_using
from pyshgp.monitoring import VerbosityConfig, DEFAULT_VERBOSITY_LEVELS


# @TODO: Should SearchConfiguration be JSON serializable?
class SearchConfiguration:
    """Configuration of an search algorithm.

    Parameters
    ----------
    evaluator : Evaluator
        The Evaluator to use when evaluating individuals.
    spawning : GeneSpawner
        The GeneSpawner to use when producing Genomes during initialization and
        variation.
    selection : Union[Selector, DiscreteProbDistrib, str], optional
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
    simplification_steps : int, optional
        The number of simplification iterations to apply to the best Push program
        produced by the search algorithm. Default is 2000.
    verbosity_config :  Union[VerbosityConfig, str], optional
        A VerbosityConfig controling what is logged during the search. Default
        is no verbosity.

    """

    def __init__(self,
                 evaluator: Evaluator,
                 spawner: GeneSpawner,
                 selection: Union[Selector, DiscreteProbDistrib, str] = "lexicase",
                 variation: Union[VariationOperator, DiscreteProbDistrib, str] = "umad",
                 population_size: int = 500,
                 max_generations: int = 100,
                 error_threshold: float = 0.0,
                 initial_genome_size: Tuple[int, int] = (10, 50),
                 simplification_steps: int = 2000,
                 verbosity_config: Union[VerbosityConfig, str] = "default",
                 **kwargs):
        self.evaluator = evaluator
        self.spawner = spawner
        self.population_size = population_size
        self.max_generations = max_generations
        self.error_threshold = error_threshold
        self.initial_genome_size = initial_genome_size
        self.simplification_steps = simplification_steps
        self.ext = kwargs

        if isinstance(selection, Selector):
            self._selection = DiscreteProbDistrib().add(selection, 1.0)
        elif isinstance(selection, DiscreteProbDistrib):
            self._selection = selection
        else:
            selector = get_selector(selection, **self.ext)
            self._selection = DiscreteProbDistrib().add(selector, 1.0)

        if isinstance(variation, VariationOperator):
            self._variation = DiscreteProbDistrib().add(variation, 1.0)
        elif isinstance(variation, DiscreteProbDistrib):
            self._variation = variation
        else:
            variationOp = get_variation_operator(variation, **self.ext)
            self._variation = DiscreteProbDistrib().add(variationOp, 1.0)

        if verbosity_config == "default":
            self.verbosity_config = DEFAULT_VERBOSITY_LEVELS[0]
        else:
            self.verbosity_config = verbosity_config

    def get_selector(self):
        """Return a Selector."""
        return self._selection.sample()

    def get_variation_op(self):
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
            spawner = self.config.spawner
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

    def _full_step(self) -> bool:
        self.generation += 1
        self.population.evaluate(self.config.evaluator)

        best_this_gen = self.population.best()
        if self.best_seen is None or best_this_gen.total_error < self.best_seen.total_error:
            self.best_seen = best_this_gen
            if self.best_seen.total_error <= self.config.error_threshold:
                return False

        if self.config.verbosity_config.generation and \
           self.generation % self.config.verbosity_config.every_n_generations == 0:
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
            self.config.verbosity_config.generation(" | ".join(stat_logs))

        self.step()
        return True

    def _is_solved(self):
        return self.best_seen.total_error <= self.config.error_threshold

    def run(self):
        """Run the algorithm until termination."""
        while self._full_step():
            if self.generation >= self.config.max_generations:
                break

        verbose_solution = self.config.verbosity_config.solution_found
        if verbose_solution:
            if self._is_solved():
                verbose_solution("Unsimplified solution found.")
            else:
                verbose_solution("No unsimplified solution found.")

        # Simplify the best individual for a better generalization and interpreteation.
        simplifier = GenomeSimplifier(self.config.evaluator, self.config.verbosity_config)
        simp_genome, simp_error_vector = simplifier.simplify(
            self.best_seen.genome,
            self.best_seen.error_vector,
            self.config.simplification_steps
        )
        simplified_best = Individual(simp_genome)
        simplified_best.error_vector = simp_error_vector

        if verbose_solution:
            if self._is_solved():
                verbose_solution("Simplified solution found.")
            else:
                verbose_solution("No simplified solution found.")

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
        op = self.config.get_variation_op()
        selector = self.config.get_selector()
        parent_genomes = [p.genome for p in selector.select(self.population, n=op.num_parents)]
        child_genome = op.produce(parent_genomes, self.config.spawner)
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
        if np.isinf(current_error) or next_error < current_error:
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
            self.config.get_variation_op().produce(
                [self.population.best().genome],
                self.config.spawner
            )
        )
        candidate.error_vector = self.config.evaluator.evaluate(candidate.program)

        acceptance_probability = self._acceptance(candidate.total_error)
        if np.random.random() < acceptance_probability:
            self.population = Population().add(candidate)


# @TODO: class EvolutionaryStrategy(SearchAlgorithm):
#     ...


def get_search_algo(name: str, **kwargs) -> SearchAlgorithm:
    """Return the search algorithm class with the given name."""
    name_to_cls = {
        "GA": GeneticAlgorithm,
        "SA": SimulatedAnnealing,
        # "ES": EvolutionaryStrategy,
    }
    _cls = name_to_cls.get(name, None)
    if _cls is None:
        raise ValueError("No search algo '{nm}'. Supported names: {lst}.".format(
            nm=name,
            lst=list(name_to_cls.keys())
        ))
    return instantiate_using(_cls, kwargs)
