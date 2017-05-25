# _*_ coding: utf_8 _*_
"""
The :mod:`selection` module defines the various selection methods supported
by pyshgp.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random
import numpy as np

from .. import exceptions as e
from . import Genetics as gen

class Selector:
    """
    """

    def __init__(self, method='lexicase', epsilon='auto', tournament_size=7):
        if method == 'lexicase':
            self._method = self._lexicase_selection
        else if method == 'epsilon_lexicase':
            self._method = self._epsilon_lexicase_selection
        else if method == 'tournament':
            self._method = self._tournament_selection

        # Sets all parameters needed for selection function.
        for arg, val in args.items():
            setattr(self, arg, val)

    def select(self, population, k):
        """

        :param list population: List of individuals.
        :param int k: Number of individuals to select.
        :returns: *k* inidividuals from *population* selected by selection method.
        """
        if self.method == 'lexicase':
            return [self._lexicase_selection(population)
                    for i in list(range(k))]
        else if method == 'epsilon_lexicase':
            return [self._epsilon_lexicase_selection(population)
                    for i in list(range(k))]
        else if method == 'tournament':
            return [self._method(population) for i in list(range(k))]

    def _lexicase_selection(self, individuals):
        """Returns an individual that does the best on the fitness cases when
        considered one at a time in random order.

        http://faculty.hampshire.edu/lspector/pubs/lexicase-IEEE-TEC.pdf

        :param list individuals: A list of individuals to select from.
        :returns: A list of selected individuals.
        """
        candidates = individuals
        cases = list(range(len(individuals[0].get_errors())))
        random.shuffle(cases)
        while len(cases) > 0 and len(candidates) > 1:
            best_val_for_case = min([ind.get_errors()[cases[0]] for ind in candidates])
            test = lambda i: i.get_errors()
            candidates = [ind for ind in candidates if ind.get_errors()[cases[0]] == best_val_for_case]
            cases.pop(0)
        return random.choice(candidates)

    def _epsilon_lexicase_selection(self, individuals):
        """Returns an individual that does the best on the fitness cases when
        considered one at a time in random order. Requires a epsilon parameter.

        :param list individuals: A list of individuals to select from.
        :param float epsilon: If an individual is within epsilon of being elite,
        it will remain in the selection pool. If 'auto', epsilon is set at the
        start of each selection even.
        :returns: A list of selected individuals.
        """
        # Check that epsilon is set
        if not hasattr(self, 'epsilon'):
            raise AttributeError('Attribute `epsilon` not defined.')

        candidates = individuals[:]
        cases = list(range(len(candidates[0].error_vector)))
        random.shuffle(cases)

        if epsilon == 'auto':
            all_errors = np.array([i.get_errors() for i in candidates])
            epsilon = np.apply_along_axis(u.median_absolute_deviation, 0,
                                          all_errors)

        while len(cases) > 0 and len(candidates) > 1:
            case = cases[0]
            errors_this_case = [i.error_vector[case] for i in candidates]
            best_val_for_case = min(errors_this_case)
            max_error = best_val_for_case + epsilon
            test = lambda i: i.error_vector[case] <= max_error
            candidates = [i for i in candidates if test(i)]
            cases.pop(0)
        return random.choice(candidates)


    def _tournament_selection(self, individuals):
        """Returns k individuals that do the best out of their respective
        tournament.

        :param list individuals: A list of individuals to select from.
        :param int tournament_size: Size of each tournament.
        :returns: A list of selected individuals.
        """
        # Check that tournament_size is set
        if not hasattr(self, 'tournament_size'):
            raise AttributeError('Attribute `tournament_size` not defined.')

        tournament = []
        for _ in range(self.tournament_size):
            tournament.append(random.choice(individuals))
        min_error_in_tourn = min([ind.get_total_error() for ind in tournament])
        best_in_tourn = [ind for ind in tournament if ind.get_total_error() == min_error_in_tourn]
        return best_in_tourn[0]
