"""The :mod:`selection` module defines classes to select Individuals from Populations."""
from abc import ABC, abstractmethod
from typing import Sequence, Union
from operator import attrgetter

import numpy as np
from numpy.random import random, choice, shuffle

from pyshgp.gp.individual import Individual
from pyshgp.gp.population import Population


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

    See: https://ieeexplore.ieee.org/document/6920034
    """

    # @TODO: Describe lexicase selection in the docstring.

    def __init__(self, epsilon: Union[bool, float, np.ndarray] = False):
        self.epsilon = epsilon

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
        candidates = population
        cases = np.arange(len(population[0].error_vector))
        shuffle(cases)

        all_errors = np.array([i.error_vector for i in candidates])

        if isinstance(self.epsilon, np.ndarray):
            ep = np.apply_along_axis(median_absolute_deviation, 0, all_errors)
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
