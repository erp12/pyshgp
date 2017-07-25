"""
The evolvers module contains classes which can be used to start PushGP runs
using the pyshgp framework.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.utils import validation, check_X_y

from .base import (PyshBase, PyshEstimatorMixin, DEFAULT_GENETICS,
                   DEFAULT_ATOM_GENERATORS, REGRESSION_ATOM_GENERATORS,
                   CLASSIFICATION_ATOM_GENERATORS)
from .population import Population
from .simplification import simplify_by_function, simplify_by_dataset


class SimplePushGPEvolver(PyshBase):
    """A simple evolutionary aglorithm to evolve a push program based on a
    error function.

    Parameters
    ----------
    atom_generators : list or str, optional (default='default')
        Atom generators used to generate random Push programs. If ``'default'``
        then all atom generators are used.

    operators : list or str, optional (default='default')
        List of tuples. Each tuple contains a VariationOperator and a float. The
        float determines the relative probability of using the VariationOperator
        to produce a child. If ``'default'`` a commonly used set of genetic
        operators is used.

    error_threshold : int or float, optional (default=0)
        If a program's total error is ever less than or equal to this value, the
        program is considered a solution.

    max_generations : int, optional (default=1000)
        Max number of generation before stopping evolution.

    population_size : int, optional (default=300)
        Number of Individuals to have in the population at any given generation.

    selection_method : str, optional (default='lexicase')
        Method to use when selecting parents. Supported options are 'lexicase',
        'epsilon_lexicase', and 'tournament'.

    n_jobs : int or str, optional (default=1)
        Number of processes to run at once during program evaluation. If ``-1``
        the number of processes will be equal to the number of cores.

    initial_max_genome_size : int, optional (default=50)
        Max number of genes to have in each randomly generated genome.

    program_growth_cap : int, optional (default=100)
        TODO: Implement this feature.

    verbose : int, optional (default=0)
        If 1, will print minimal information while evolving. If 2, will print
        as much information as possible during evolution however this might
        slightly impact runtime. If 0, prints nothing during evolution.

    epsilon : float or str, optional (default='auto')
        The value of epsilon when using 'epsilon_lexicase' as the selection
        method. If `auto`, epsilon is set to be equal to the Median Absolute
        Deviation of each error.

    tournament_size : int, optional (default=7)
        The size of each tournament when using 'tournament' selection.

    simplification_steps : int, optional (default=2000)
        Number of steps of automatic program simplification to perform.

    Attributes
    ----------

    best_ : Individual
        Best Individual present in the last generation of evolution.

    best_error_ : float
        Total error of the Individual stored in best_. This is considered the
        overall training error of the SymbolicRegressor.

    """

    def __init__(self, atom_generators='default', operators='default',
                 error_threshold=0, max_generations=1000,
                 population_size=300, selection_method='epsilon_lexicase',
                 n_jobs=1, initial_max_genome_size=50,
                 program_growth_cap=100, verbose=0,
                 epsilon='auto', tournament_size=7, simplification_steps=2000):

        if atom_generators == 'default':
            atom_generators = DEFAULT_ATOM_GENERATORS

        if operators == 'default':
            operators = DEFAULT_GENETICS

        PyshBase.__init__(self, atom_generators=atom_generators,
                          operators=operators,
                          max_generations=max_generations,
                          population_size=population_size,
                          selection_method=selection_method,
                          n_jobs=n_jobs, program_growth_cap=program_growth_cap,
                          initial_max_genome_size=initial_max_genome_size,
                          verbose=verbose,
                          simplification_steps=simplification_steps,
                          epsilon=epsilon, tournament_size=tournament_size)

    def _evaluation(self, error_function):
        """Evaluates the population using an error function. If a process pool
        is setup, then evaluation is parallelized using it.

        TODO: Check for population.

        Parameters
        ----------
        error_function : function
            A function with takes a push program as input and returns an error
            vector.
        """
        if hasattr(self, 'pool'):
            self.population.evaluate_by_function(error_function, self.pool)
        else:
            self.population.evaluate_by_function(error_function)

    def _simplification(self, error_function):
        """Evaluates the population.

        Parameters
        ----------
        error_function : function
            A function with takes a push program as input and returns an error
            vector.
        """
        validation.check_is_fitted(self, 'best_')
        simplify_by_function(self.best_, error_function,
                             self.simplification_steps, self.verbose)

    def fit(self, error_function, n_inputs, output_types):
        """Fits the SimplePushGPEvolver.

        Parameters
        ----------
        error_function : function
            A function with takes a push program as input and returns an error
            vector.

        n_inputs : int
            The number of input values that will be provided to the evolved
            push programs.

        output_types : list
            A list of pysh types. The spawner will include instructions which
            ouput a list of outputs with the corresponding type in each index.
        """
        self.output_types = output_types
        self.make_spawner(n_inputs, output_types)
        self.init_population()
        self._evaluation(error_function)

        for g in range(self.max_generations):

            # Verbose mode monitor printing
            if self.verbose == 1:
                self.print_monitor(g)
            elif self.verbose > 1:
                self.print_monitor_verbose(g)

            # Check for solution
            if self.population.lowest_error() <= self.error_threshold:
                break

            # Create next generation
            next_gen = Population()
            for i in range(self.population_size):
                op = self.choose_genetic_operator()

                parents = [
                    self.population.select(self.selection_method,
                                           self.epsilon,
                                           self.tournament_size)
                    for p in range(op._num_parents)
                ]
                next_gen.append(op.produce(parents, self.spawner))
            self.population = next_gen

            # Evaluate the population
            self._evaluation(error_function)

        self.best_error_ = min([i.total_error for i in self.population])

        def test(i): return i.total_error == self.best_error_
        self.best_ = [i for i in self.population if test(i)][0]
        self._simplification(error_function)
        return self

    def predict(self, X):
        """Predict using the best program found by evolution.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        Returns
        -------
        C : array, shape = (n_samples,)
            Returns predicted values.
        """
        validation.check_is_fitted(self, 'best_')

        def f(x):
            return self.best_.run_program(x, self.output_types)
        return np.apply_along_axis(f, 1, X)


class PushGPRegressor(PyshBase, PyshEstimatorMixin, BaseEstimator,
                      RegressorMixin):
    """A Scikit-learn estimator that uses PushGP for regression tasks.

    Parameters
    ----------
    fit_metric : function
        A sklearn scoring function to use when calculating an Individual's
        total error.

    atom_generators : list or str, optional (default='default')
        Atom generators used to generate random Push programs. If ``'default'``
        then all atom generators are used.

    operators : list or str, optional (default='default')
        List of tuples. Each tuple contains a VariationOperator and a float. The
        float determines the relative probability of using the VariationOperator
        to produce a child. If ``'default'`` a commonly used set of genetic
        operators is used.

    error_threshold : int or float, optional (default=0)
        If a program's total error is ever less than or equal to this value, the
        program is considered a solution.

    max_generations : int, optional (default=1000)
        Max number of generation before stopping evolution.

    population_size : int, optional (default=300)
        Number of Individuals to have in the population at any given generation.

    selection_method : str, optional (default='lexicase')
        Method to use when selecting parents. Supported options are 'lexicase',
        'epsilon_lexicase', and 'tournament'.

    n_jobs : int or str, optional (default=1)
        Number of processes to run at once during program evaluation. If ``-1``
        the number of processes will be equal to the number of cores.

    initial_max_genome_size : int, optional (default=50)
        Max number of genes to have in each randomly generated genome.

    program_growth_cap : int, optional (default=100)
        TODO: Implement this feature.

    verbose : int, optional (default=0)
        If 1, will print minimal information while evolving. If 2, will print
        as much information as possible during evolution however this might
        slightly impact runtime. If 0, prints nothing during evolution.

    epsilon : float or str, optional (default='auto')
        The value of epsilon when using 'epsilon_lexicase' as the selection
        method. If `auto`, epsilon is set to be equal to the Median Absolute
        Deviation of each error.

    tournament_size : int, optional (default=7)
        The size of each tournament when using 'tournament' selection.

    simplification_steps : int, optional (default=2000)
        Number of steps of automatic program simplification to perform.

    Attributes
    ----------

    best_ : Individual
        Best Individual present in the last generation of evolution.

    best_error_ : float
        Total error of the Individual stored in best_. This is considered the
        overall training error of the SymbolicRegressor.
    """

    def __init__(self, atom_generators='default',
                 operators='default', error_threshold=1e-5,
                 max_generations=1000, population_size=500,
                 selection_method='epsilon_lexicase', n_jobs=1,
                 initial_max_genome_size=50, program_growth_cap=100,
                 verbose=0, epsilon='auto', tournament_size=7,
                 simplification_steps=500):

        if atom_generators == 'default':
            atom_generators = REGRESSION_ATOM_GENERATORS

        if operators == 'default':
            operators = DEFAULT_GENETICS

        PyshBase.__init__(self,  atom_generators=DEFAULT_ATOM_GENERATORS,
                          operators=DEFAULT_GENETICS,
                          error_threshold=error_threshold,
                          max_generations=max_generations,
                          population_size=population_size,
                          selection_method=selection_method, n_jobs=n_jobs,
                          program_growth_cap=program_growth_cap,
                          initial_max_genome_size=initial_max_genome_size,
                          verbose=verbose, epsilon=epsilon,
                          simplification_steps=simplification_steps,
                          tournament_size=tournament_size)
        self.output_types = ['_float']

    def _evaluation(self, X, y):
        """Evaluates the population.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Target values.
        """
        if hasattr(self, 'pool'):
            self.population.evaluate_by_dataset(X, y, 'regression', self.pool)
        else:
            self.population.evaluate_by_dataset(X, y, 'regression')

    def _simplification(self, X, y):
        """Simplifies the program of the best individual found during evolution.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Target values.
        """
        validation.check_is_fitted(self, 'best_')
        self.best_ = simplify_by_dataset(self.best_, X, y,
                                         'regression',
                                         self.simplification_steps,
                                         self.verbose)

    def fit(self, X, y):
        """Fits the PushGPRegressor.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Target values.
        """
        X, y = check_X_y(X, y)
        n_feats = X.shape[1]
        self.make_spawner(n_feats, self.output_types)
        return self.evolve(X, y)

    def predict(self, X):
        """Predict using the best program found by evolution.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        Returns
        -------
        C : array, shape = (n_samples,)
            Returns predicted values.
        """
        validation.check_is_fitted(self, 'best_')

        def f(x):
            return self.best_.run_program(x, self.output_types)[0]
        return np.apply_along_axis(f, 1, X)


class PushGPClassifier(PyshBase, PyshEstimatorMixin, BaseEstimator,
                       ClassifierMixin):
    """A Scikit-learn estimator that uses PushGP for regression tasks.

    Parameters
    ----------
    fit_metric : function, optional (default=sklearn.metrics.accuracy_score)
        A sklearn scoring function to use when calculating an Individual's
        total error.

    atom_generators : list or str, optional (default='default')
        Atom generators used to generate random Push programs. If ``'default'``
        then all atom generators are used.

    operators : list or str, optional (default='default')
        List of tuples. Each tuple contains a VariationOperator and a float. The
        float determines the relative probability of using the VariationOperator
        to produce a child. If ``'default'`` a commonly used set of genetic
        operators is used.

    error_threshold : int or float, optional (default=0)
        If a program's total error is ever less than or equal to this value, the
        program is considered a solution.

    max_generations : int, optional (default=1000)
        Max number of generation before stopping evolution.

    population_size : int, optional (default=300)
        Number of Individuals to have in the population at any given generation.

    selection_method : str, optional (default='lexicase')
        Method to use when selecting parents. Supported options are 'lexicase',
        'epsilon_lexicase', and 'tournament'.

    n_jobs : int or str, optional (default=1)
        Number of processes to run at once during program evaluation. If ``-1``
        the number of processes will be equal to the number of cores.

    initial_max_genome_size : int, optional (default=50)
        Max number of genes to have in each randomly generated genome.

    program_growth_cap : int, optional (default=100)
        TODO: Implement this feature.

    verbose : int, optional (default=0)
        If 1, will print minimal information while evolving. If 2, will print
        as much information as possible during evolution however this might
        slightly impact runtime. If 0, prints nothing during evolution.

    epsilon : float or str, optional (default='auto')
        The value of epsilon when using 'epsilon_lexicase' as the selection
        method. If `auto`, epsilon is set to be equal to the Median Absolute
        Deviation of each error.

    tournament_size : int, optional (default=7)
        The size of each tournament when using 'tournament' selection.

    simplification_steps : int, optional (default=2000)
        Number of steps of automatic program simplification to perform.

    Attributes
    ----------

    best_ : Individual
        Best Individual present in the last generation of evolution.

    best_error_ : float
        Total error of the Individual stored in best_. This is considered the
        overall training error of the SymbolicRegressor.
    """

    def __init__(self, atom_generators='default',
                 operators='default', error_threshold=1e-5,
                 max_generations=1000, population_size=500,
                 selection_method='epsilon_lexicase', n_jobs=1,
                 initial_max_genome_size=50, program_growth_cap=100,
                 verbose=0, epsilon='auto', tournament_size=7,
                 simplification_steps=500):

        if atom_generators == 'default':
            atom_generators = CLASSIFICATION_ATOM_GENERATORS

        if operators == 'default':
            operators = DEFAULT_GENETICS

        PyshBase.__init__(self,  atom_generators=DEFAULT_ATOM_GENERATORS,
                          operators=DEFAULT_GENETICS,
                          error_threshold=error_threshold,
                          max_generations=max_generations,
                          population_size=population_size,
                          selection_method=selection_method, n_jobs=n_jobs,
                          program_growth_cap=program_growth_cap,
                          initial_max_genome_size=initial_max_genome_size,
                          verbose=verbose, epsilon=epsilon,
                          simplification_steps=simplification_steps,
                          tournament_size=tournament_size)

    def _evaluation(self, X, y):
        """Evaluates the population.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Target values.
        """
        if hasattr(self, 'pool'):
            self.population.evaluate_by_dataset(X, y, 'classification',
                                                self.pool)
        else:
            self.population.evaluate_by_dataset(X, y, 'classification')

    def _simplification(self, X, y):
        """Simplifies the program of the best individual found during evolution.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Target values.
        """
        validation.check_is_fitted(self, 'best_')
        self.best_ = simplify_by_dataset(self.best_, X, y,
                                         'classification',
                                         self.simplification_steps,
                                         self.verbose)

    def fit(self, X, y):
        """Fits the PushGPClassifier.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Target values.
        """
        X, y = check_X_y(X, y)
        n_feats = X.shape[1]
        n_classes = len(np.unique(y))
        self.output_types = ['_class'] * n_classes
        self.make_spawner(n_feats, self.output_types)
        return self.evolve(X, y)

    def predict(self, X):
        """Predict using the best program found by evolution.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        Returns
        -------
        C : array, shape = (n_samples,)
            Returns predicted values.
        """
        validation.check_is_fitted(self, 'best_')

        def f(x):
            output_vector = self.best_.run_program(x, self.output_types)
            not_none = [x for x in output_vector if x is not None]
            if len(not_none) == 0:
                return None
            else:
                return output_vector.index(max(not_none))
        return np.apply_along_axis(f, 1, X)
