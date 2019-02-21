"""The :mod:`selection` module defines classes to select Individuals from Populations."""
from abc import ABC, abstractmethod
from typing import Sequence, Union
from operator import attrgetter

import numpy as np
from numpy.random import random, choice, shuffle

from pyshgp.gp.individual import Individual
from pyshgp.gp.population import Population
from pyshgp.utils import instantiate_using


class Selector(ABC):
    """Base class for all selection algorithms."""

    @abstractmethod
    def select_one(self, population: Population) -> Individual:
        """Return single individual from population.

        Parameters
        ----------
        population
            A Population of Individuals.

        Returns
        -------
        Individual
            The selected Individual.

        """
        pass

    def select(self, population: Population, n: int = 1) -> Sequence[Individual]:
        """Return `n` individuals from the population.

        Parameters
        ----------
        population
            A Population of Individuals.

        Returns
        -------
        Sequence[Individual]
            The selected Individuals.

        """
        selected = []
        for i in range(n):
            selected.append(self.select_one(population))
        return selected


# @TODO: class SelectorPipeline(Selector)


class FitnessProportionate(Selector):
    """Fitness proportionate selection, also known as roulette wheel selection.

    See: https://en.wikipedia.org/wiki/Fitness_proportionate_selection
    """

    def select_one(self, population: Population) -> Individual:
        """Return single individual from population.

        Parameters
        ----------
        population
            A Population of Individuals.

        Returns
        -------
        Individual
            The selected Individual.

        """
        return self.select(population)[0]

    def select(self, population: Population, n: int = 1) -> Sequence[Individual]:
        """Return `n` individuals from the population.

        Parameters
        ----------
        population
            A Population of Individuals.

        Returns
        -------
        Sequence[Individual]
            The selected Individuals.

        """
        population_total_errors = np.array([i.total_error for i in population])
        sum_of_total_errors = np.sum(population_total_errors)
        probablilities = 1.0 - (population_total_errors / sum_of_total_errors)
        selected_ndxs = np.searchsorted(np.cumsum(probablilities), random(n))
        return [population[ndx] for ndx in selected_ndxs]


class Tournament(Selector):
    """Tournament selection.

    See: https://en.wikipedia.org/wiki/Tournament_selection

    Parameters
    ----------
    tournament_size : int, optional
        Number of individuals selected uniformly randomly to participate in
        the tournament. Default is 7.

    Attributes
    ----------
    tournament_size : int, optional
        Number of individuals selected uniformly randomly to participate in
        the tournament. Default is 7.

    """

    def __init__(self, tournament_size: int = 7):
        self.tournament_size = tournament_size

    def select_one(self, population: Population) -> Individual:
        """Return single individual from population.

        Parameters
        ----------
        population
            A Population of Individuals.

        Returns
        -------
        Individual
            The selected Individual.

        """
        tournament = choice(population, self.tournament_size, replace=False)
        return min(tournament, key=attrgetter('total_error'))


def median_absolute_deviation(x: np.ndarray) -> np.float64:
    """Return the MAD.

    Parameters
    ----------
    a : array-like, shape = (n,)

    Returns
    -------
    mad : float

    """
    return np.median(np.abs(x - np.median(x)))


class Lexicase(Selector):
    """Lexicase Selection.

    All training cases are considered iteratively in a random order. For each
    training cases, the population is filtered to only contain the Individuals
    which have an error value within epsilon of the best error value on that case.
    This filtering is repeated until the population is down to a single Individual
    or all cases have been used. After the filtering iterations, a random
    Individual from the remaining set is returned as the selected Individual.

    See: https://ieeexplore.ieee.org/document/6920034
    """

    def __init__(self, epsilon: Union[bool, float, np.ndarray] = False):
        self.epsilon = epsilon

    def _preselection(self, population: Population) -> Sequence[Individual]:
        """Preselect one individual per distinct error vector.

        Crucial for avoiding the worst case runtime of lexicase selection but
        does not impact the behavior of which indiviudal gets selected.
        """
        population_list = list(population)
        shuffle(population_list)
        preselected = []
        error_vector_hashes = []
        for individual in population_list:
            error_vector_hash = hash(individual.error_vector_bytes)
            if error_vector_hash not in error_vector_hashes:
                preselected.append(individual)
                error_vector_hashes.append(error_vector_hash)
        return preselected

    def select_one(self, population: Population) -> Individual:
        """Return single individual from population.

        Parameters
        ----------
        population
            A Population of Individuals.

        Returns
        -------
        Individual
            The selected Individual.

        """
        candidates = self._preselection(population)
        cases = np.arange(len(population[0].error_vector))
        shuffle(cases)

        if isinstance(self.epsilon, np.ndarray):
            ep = np.apply_along_axis(median_absolute_deviation, 0, population.all_error_vectors())
        elif isinstance(self.epsilon, (float, int, np.int64, np.float64)):
            ep = self.epsilon

        while len(cases) > 0 and len(candidates) > 1:
            case = cases[0]
            errors_this_case = [i._error_vector[case] for i in candidates]
            best_val_for_case = min(errors_this_case)

            if isinstance(self.epsilon, np.ndarray):
                max_error = best_val_for_case + ep[case]
            elif isinstance(self.epsilon, (float, int, np.int64, np.float64)):
                max_error = best_val_for_case + ep
            else:
                max_error = best_val_for_case

            candidates = [i for i in candidates if i._error_vector[case] <= max_error]
            cases = cases[1:]
        return choice(candidates)


class Elite(Selector):
    """Returns the best N individuals by total error."""

    def select_one(self, population: Population) -> Individual:
        """Return single individual from population.

        Parameters
        ----------
        population
            A Population of Individuals.

        Returns
        -------
        Individual
            The selected Individual.

        """
        return population.best()

    def select(self, population: Population, n: int = 1) -> Sequence[Individual]:
        """Return `n` individuals from the population.

        Parameters
        ----------
        population
            A Population of Individuals.

        Returns
        -------
        Sequence[Individual]
            The selected Individuals.

        """
        return population.best_n(n)


def get_selector(name: str, **kwargs) -> Selector:
    """Get the selector class with the given name."""
    name_to_cls = {
        "roulette": FitnessProportionate,
        "tournament": Tournament,
        "lexicase": Lexicase,
        "elite": Elite,
    }
    _cls = name_to_cls.get(name, None)
    if _cls is None:
        raise ValueError("No selector '{nm}'. Supported names: {lst}.".format(
            nm=name,
            lst=list(name_to_cls.keys())
        ))
    return instantiate_using(_cls, kwargs)
