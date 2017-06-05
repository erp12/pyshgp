"""
Classes that reperesents Individuals and Populations in evolutionary algorithms.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import math, random
from copy import copy, deepcopy
import numpy as np

from ..utils import (keep_number_reasonable, median_absolute_deviation,
                     UnevaluatableStackResponse, levenshtein_distance,
                     is_int_type, is_str_type, count_points)
from ..push import translation as tran
from ..push import interpreter as interp
from .simplification import simplify_once

###########
# Classes #
###########

class Individual(object):
    """Holds all information about an individual.

    TODO: Write attribute docstrings
	"""

    _genome = None
    _program = None

    # Genome
    @property
    def genome(self):
        """Plush Genome of individual.
        """
        return self._genome

    @genome.setter
    def genome(self, value):
        self._genome = value
        self._program = tran.genome_to_program(value)

    # Program
    @property
    def program(self):
        """Push program of individual. Taken from Plush genome.
        """
        return self._program

    @program.setter
    def program(self, value):
        raise AttributeError("Cannot set Individual's program directly. Must \
                             set genome.")

    def __init__(self, genome):
        self.genome = genome

    def __repr__(self):
        return "PyshIndividual<"+str(self.total_error)+">"

    def sync_program_to_genome(self):
        """If single genes of a
        """

    def run_program(self, inputs=[], print_trace=False):
        """Runs the Individual's program.

        :param list inputs: List of input values that can be accessed by the
        Individual's program.
        :param bool print_trace: If true, prints the current program element and
        the state of the stack at each step of executing the program. Defaults
        to False.
        :returns: The final state of the push Interpreter after executing the
        program.
        """
        i = interp.PushInterpreter(inputs)
        return i.run_push(self.program, print_trace)

    def evaluate(self, X, y, metric=None):
        """Evaluates the individual.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Labels.

        output_dict : dict
            Name of stack which will contain the output values.

        metric : function
            Function to used to calculate the error of the individual. Sklearn
            scoring functions are supported.
        """
        y_hat = []
        error_vec = []
        for i in range(X.shape[0]):
            result = self.run_program(X[i])
            outputs = list(result.values())
            y_hat.append(outputs)
            targets = list(y[i])
            for j in range(len(outputs)):
                if is_int_type(outputs[j]) or isinstance(outputs[j], (float, np.float)):
                    error_vec.append(abs(outputs[j] - targets[j]))
                elif is_str_type(outputs[j]):
                    levenshtein_distance(outputs[j], targets[j])
        self.error_vector = error_vec
        if metric is None:
            self.total_error = sum(self.error_vector)
        else:
            self.total_error = metric(y, y_hat)
        return self

    def evaluate_with_function(self, error_function):
        """Evaluates the individual by passing it's program to the error
        function.

        :param func error_function: The error function.
        """
        errs = error_function(self.program)
        self.error_vector = errs
        self.total_error = sum(self.error_vector)
        return self

    def simplify(self, X, y, metric=None, steps=2000, verbose=0):
        """Simplifies the genome (and program) of the individual based on
        a dataset by randomly removing some elements of the program and
        confirming that the total error remains the same or lower. This is
        acheived by silencing some genes in the individual's genome.
        """
        # Print the origional size of the individual.
        if verbose > 0:
            print("Autosimplifying program of size:",
                  count_points(self.program))
        for i in range(steps):
            orig_err = copy(self.total_error)
            orig_gn = copy(self.genome)
            # Evalaute the current individual and copy of the genome and error.
            self.evaluate(X, y, metric)
            self.genome = simplify_once(self.genome)
            # Evaluate the individual again.
            self.evaluate(X, y, metric)
            # Decide if the simplification impacted performance, and revert.
            if self.total_error > orig_err:
                self.genome = orig_gn
        # Print the final size of the individual.
        if verbose > 0:
            print("Finished simplifying program. New size:",
                  count_points(self.program))
            print(self.program)

    def simplify_with_function(self, error_function, steps=2000, verbose=0):
        """Simplifies the genome (and program) of the individual based on
        an error function by randomly removing some elements of the program and
        confirming that the total error remains the same or lower. This is
        acheived by silencing some genes in the individual's genome.
        """
        # Print the origional size of the individual.
        if verbose > 0:
            print("Autosimplifying program of size:",
                  count_points(self.program))
        for i in range(steps):
            orig_err = copy(self.total_error)
            orig_gn = deepcopy(self.genome)
            # Evalaute the current individual and copy of the genome and error.
            self.evaluate_with_function(error_function)
            self.genome = simplify_once(self.genome)
            # Evaluate the individual again.
            self.evaluate_with_function(error_function)
            # Decide if the simplification impacted performance, and revert.
            print(orig_err, self.total_error, '||', count_points(self.program))
            if self.total_error > orig_err:
                print('REVERT')
                self.genome = orig_gn
        # Print the final size of the individual.
        if verbose > 0:
            print("Finished simplifying program. New size:",
                  count_points(self.program))
            print(self.program)

class Population(list):
    """Pyshgp population of Individuals.
    """

    def evaluate(self, X, y, metric):
        """Evaluates every individual in the population, if the individual has
        not been previously evaluated.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Target values.

        metric : function
            Function to used to calculate the error of an individual. All
            sklearn regression metrics are supported.
        """
        def f(i):
            if not hasattr(i, 'error_vector'):
                return i.evaluate(X, y, metric)
            return i

        if not pool is None:
            self[:] = pool.map(f, self)
        else:
            for i in self:
                f(i)

    def evaluate_with_function(self, error_function, pool=None):
        """Evaluates every individual in the population, if the individual has
        not been previously evaluated.

        :param func error_function: The error function.
        """
        def f(i):
            if not hasattr(i, 'error_vector'):
                return i.evaluate_with_function(error_function)
            return i

        if not pool is None:
            self[:] = pool.map(f, self)
        else:
            for i in self:
                f(i)

    def select(self, method='lexicase', epsilon='auto', tournament_size=7):
        """Selects a individual from the population with the given selection
        method.

        TODO: Write method docstring.
        """
        if method == 'epsilon_lexicase':
            return self.epsilon_lexicase_selection(epsilon)
        elif method == 'lexicase':
            return self.lexicase_selection()
        elif method == 'tournament':
            return self.tournament_selection(tournament_size)
        else:
            raise ValueError("Unknown selection method: " + str(method))

    def lexicase_selection(self):
        """Returns an individual that does the best on the fitness cases when
        considered one at a time in random order.

        http://faculty.hampshire.edu/lspector/pubs/lexicase-IEEE-TEC.pdf

        Returns
        -------
        individual : Individual
            An individual from the population selected using lexicase selection.
        """
        candidates = self[:]
        cases = list(range(len(self[0].error_vector)))
        random.shuffle(cases)
        while len(cases) > 0 and len(candidates) > 1:
            best_val_for_case = min([ind.error_vector[cases[0]] for ind in candidates])
            candidates = [ind for ind in candidates if ind.error_vector[cases[0]] == best_val_for_case]
            cases.pop(0)
        return random.choice(candidates)

    def epsilon_lexicase_selection(self, epsilon='auto'):
        """Returns an individual that does the best on the fitness cases
        when considered one at a time in random order.

        Parameters
        ----------
        epsilon : {'auto', float, array-like}
            If an individual is within epsilon of being elite, it will
            remain in the selection pool. If 'auto', epsilon is set at
            the start of each selection even to be equal to the
            Median Absolute Deviation of each test case.

        Returns
        -------
        individual : Individual
            An individual from the population selected using lexicase
            selection.
        """
        candidates = self[:]
        cases = list(range(len(self[0].error_vector)))
        random.shuffle(cases)

        if epsilon == 'auto':
            all_errors = np.array([i.error_vector[:] for i in candidates])
            epsilon = np.apply_along_axis(median_absolute_deviation, 0,
                                          all_errors)

        while len(cases) > 0 and len(candidates) > 1:
            case = cases[0]
            errors_this_case = [i.error_vector[case] for i in candidates]
            best_val_for_case = min(errors_this_case)
            if isinstance(epsilon, (list, tuple, np.ndarray)):
                max_error = best_val_for_case + epsilon[case]
            else:
                max_error = best_val_for_case + epsilon
            test = lambda i: i.error_vector[case] <= max_error
            candidates = [i for i in candidates if test(i)]
            cases.pop(0)
        return random.choice(candidates)

    def tournament_selection(self, tournament_size=7):
        """Returns the individual with the lowest error within a random
        tournament.

        Parameters
        ----------
        tournament_size : int
            Size of each tournament.

        Returns
        -------
        individual : Individual
            An individual from the population selected using tournament
            selection.
        """
        tournament = []
        for _ in range(tournament_size):
            tournament.append(random.choice(self[:]))
        min_error_in_tourn = min([ind.total_error for ind in tournament])
        best_in_tourn = [ind for ind in tournament if ind.total_error == min_error_in_tourn]
        return best_in_tourn[0]

    def lowest_error(self):
        """Returns the lowest total error found in the population.
        """
        gnrtr = (ind.total_error for ind in self)
        return np.min(np.fromiter(gnrtr, np.float))

    def average_error(self):
        """Returns the average total error found in the population.
        """
        gnrtr = (ind.total_error for ind in self)
        return np.mean(np.fromiter(gnrtr, np.float))

    def unique(self):
        """Returns the number of unique programs found in the population.
        """
        programs_set = {str(ind.program) for ind in self}
        return len(programs_set)

    def best_program(self):
        """Returns the program of the Individual with the lowest total error.
        """
        e = self.lowest_error()
        test = lambda i: i.total_error == e
        return [i.program for i in self if test(i)][0]
