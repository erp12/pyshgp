"""
Classes that reperesents Individuals and Populations in evolutionary
algorithms.
"""
import random
import numpy as np

from ..utils import median_absolute_deviation
from ..push import translation as tran
from ..push import interpreter as interp
from .evaluate import (
    evaluate_with_function,
    evaluate_for_regression,
    evaluate_for_classification
)

###########
# Classes #
###########


class Individual(object):
    """Holds all information about an individual in the PushGP framework.

    The main role of an Individual is to hold a Push program that determines
    the Individual's behavior. An Individual's push program comes from a Plush
    genome, which is also stored in the Individual. Genomes are what pyshgp's
    VariationOperators manipulation. An Individual is created based off a
    genome, and it's program is set by translating the genome into into a
    program.

    Parameters
    ----------
    genome : list of genes
        List of plush genes.

    Attributes
    ----------
    genome : list of genes
        List of plush genes.
    program : list
        A Push program.
    error_vector : list
        A list of numeric error values.
    total_error : float
        A single numeric error value. Generally some aggregate of the
        ``error_vector``.
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
        msg = "Cannot set Individual's program directly. Must set genome."
        raise AttributeError(msg)

    def __init__(self, genome):
        self.genome = genome

    def __repr__(self):
        return "PyshIndividual<" + str(self.total_error) + ">"

    def run_program(self, inputs, output_types, print_trace=False):
        """Runs the Individual's program.

        Parameters
        ----------
        inputs : list
            List of input values that can be accessed by the Individual's
            program.

        print_trace : bool, optional
            If ``True``, prints the current program element and the state of
            the stack at each step of executing the program.

        output_types : list
            A list of pysh types. The spawner will include instructions which
            ouput a list of outputs with the corresponding type in each index.

        Returns
        --------
        The final state of the push Interpreter after executing the program.
        """
        i = interp.PushInterpreter()
        return i.run(self.program, inputs, output_types, print_trace)


class Population(list):
    """Pyshgp population of Individuals.
    """

    def evaluate_by_dataset(self, X, y, mode, pool=None):
        """Evalutes the population based on the specified mode.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Target values.

        mode : str
            Valid options include "regression" and "classification".

        pool : pathos.multiprocessing.Pool, optional
            Pool of processes to evaluate in parallel.
        """
        evl = None
        if mode == 'regression':
            evl = evaluate_for_regression
        elif mode == 'classification':
            evl = evaluate_for_classification
        else:
            raise ValueError('Unknown evaluate_by_dataset mode.')

        def f(i):
            if not hasattr(i, 'error_vector'):
                return evl(i, X, y)
            return i

        if pool is not None:
            self[:] = pool.map(f, self)
        else:
            for i in self:
                f(i)

    def evaluate_by_function(self, error_function, pool=None):
        """Evaluates every individual in the population, if the individual has
        not been previously evaluated.

        Parameters
        ----------
        error_function : function
            The error function which takes a push program as input and Returns
            an error vector

        pool : pathos.multiprocessing.Pool, optional
            Pool of processes to evaluate in parallel.
        """
        def f(i):
            if not hasattr(i, 'error_vector'):
                return evaluate_with_function(i, error_function)
            return i

        if pool is not None:
            self[:] = pool.map(f, self)
        else:
            for i in self:
                f(i)

    def select(self, method='lexicase', epsilon='auto', tournament_size=7):
        """Selects a individual from the population with the given selection
        method.

        Parameters
        ----------
        method : str, optional (default='lexicase')
            The selection method to be used when selecting parents. Supported
            options are 'lexicase', 'epsilon_lexicase', and 'tournament'.

        epsilon : int, str, optional (default='auto')
            The value of epsilon when using 'epsilon_lexicase' as the selection
            method. If `auto`, epsilon is set to be equal to the Median
            Absolute Deviation of each error.

        tournament_size : int, optional (default=7)
            The size of each tournament when using 'tournament' selection.
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
            best_val_for_case = min([i.error_vector[cases[0]]
                                     for i in candidates])

            def test(i): return i.error_vector[cases[0]] == best_val_for_case
            candidates = [ind for ind in candidates if test(ind)]
            cases.pop(0)
        return random.choice(candidates)

    def epsilon_lexicase_selection(self, epsilon='auto'):
        """Returns an individual that does the best on the fitness cases
        when considered one at a time in random order.

        Parameters
        ----------
        epsilon : float, array-like or str, optional (default='auto')
            If an individual is within epsilon of being elite, it will remain
            in the selection pool. If 'auto', epsilon is set at the start of
            each selection even to be equal to the Median Absolute Deviation
            of each error.

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

            def test(i): return i.error_vector[case] <= (max_error + 1)
            candidates = [i for i in candidates if test(i)]
            cases.pop(0)
        return random.choice(candidates)

    def tournament_selection(self, tournament_size=7):
        """Returns the individual with the lowest error within a random
        tournament.

        Parameters
        ----------
        tournament_size : int, optional (default=7)
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

        def test(i): return i.total_error == min_error_in_tourn
        best_in_tourn = [ind for ind in tournament if test(ind)]
        return best_in_tourn[0]

    def lowest_error(self):
        """
        Returns
        -------
        The lowest total error found in the population.
        """
        gnrtr = (ind.total_error for ind in self)
        return np.min(np.fromiter(gnrtr, np.float))

    def average_error(self):
        """
        Returns
        -------
        The average total error found in the population.
        """
        gnrtr = (ind.total_error for ind in self)
        return np.mean(np.fromiter(gnrtr, np.float))

    def unique(self):
        """
        Returns
        -------
        The number of unique programs found in the population.
        """
        programs_set = {str(ind.program) for ind in self}
        return len(programs_set)

    def best_program(self):
        """
        Returns
        -------
        The program of the Individual with the lowest total error.
        """
        e = self.lowest_error()

        def test(i): return i.total_error == e
        return [i.program for i in self if test(i)][0]

    def best_program_error_vector(self):
        """
        Returns
        -------
        The program of the Individual with the lowest total error.
        """
        e = self.lowest_error()

        def test(i): return i.total_error == e
        best = [i for i in self if test(i)][0]
        return [round(x, 2) for x in best.error_vector]
