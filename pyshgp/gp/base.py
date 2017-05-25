"""
Esitmator classes for pyshgp.

TODO: Add a lot of validation checks.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import inspect
import numpy as np
from numpy.random import choice
from random import random, randint

from sklearn.base import BaseEstimator, ClassifierMixin, RegressorMixin
from sklearn.metrics import mean_squared_error, euclidean_distances
from sklearn.utils import validation, check_array

from .population import Population, Individual
from .variation import VariationOperatorPipeline, UniformMutation, Alternation
from ..push import random as r
from ..push.instruction import PyshInputInstruction, PyshClassVoteInstruction
from ..push.interpreter import PushInterpreter
from ..utils import merge_sets
from ..push.instructions import registered_instructions as ri


DEFAULT_GENETICS = [
    (Alternation(), 0.7),
    (UniformMutation(), 0.1),
    (VariationOperatorPipeline((Alternation(), UniformMutation())), 0.2)
]

DEFAULT_ATOM_GENERATORS=list(merge_sets(
    ri.registered_instructions,
    [lambda: randint(0, 100), lambda: random()]))
REGRESSION_ATOM_GENERATORS=list(merge_sets(
    ri.get_instructions_by_pysh_type('_exec'),
    ri.get_instructions_by_pysh_type('_boolean'),
    ri.get_instructions_by_pysh_type('_integer'),
    ri.get_instructions_by_pysh_type('_float'),
    [lambda: randint(0, 100), lambda: random()]))
CLASSIFICATION_ATOM_GENERATORS=list(merge_sets(
    ri.get_instructions_by_pysh_type('_exec'),
    ri.get_instructions_by_pysh_type('_boolean'),
    ri.get_instructions_by_pysh_type('_integer'),
    ri.get_instructions_by_pysh_type('_float'),
    [lambda: randint(0, 100), lambda: random()]))

class PyshMixin:
    """Contains all evoluationary

    TODO: Add validation checks.
    TODO: add attribute docstrings.
    """

    def __init__(self, error_threshold=0, max_generations=1000,
            population_size=300, selection_method='lexicase', n_jobs=1,
            operators=DEFAULT_GENETICS, initial_max_genome_size=50,
            program_growth_cap=100, atom_generators=DEFAULT_ATOM_GENERATORS,
            verbose=0, epsilon='auto', tournament_size=7,
            simplification_steps=500):
        self.error_threshold=error_threshold
        self.max_generations=max_generations
        self.population_size=population_size
        self.selection_method=selection_method
        self.n_jobs = n_jobs
        self.operators=operators
        self.initial_max_genome_size=initial_max_genome_size
        self.program_growth_cap=program_growth_cap
        self.atom_generators=atom_generators
        self.verbose=verbose
        self.epsilon=epsilon
        self.tournament_size=tournament_size,
        self.simplification_steps=simplification_steps

        if not self.n_jobs == 1:
            self.init_executor()

    def init_executor(self):
        """Initializes a pool of processes.

        This requires pathos.multiprocessing because the standard
        multiprocessing library does not support pickling lambda and non-top
        level functions. Pathos specifically makes use of the dill package.

        .. todo::
            If there is away around using pathos, it would be great to remove
            this dependency.

        :param dict max_workers: Number of worker to put in pool. -1 uses
        same number as available cores.
        """
        from pathos.multiprocessing import ProcessingPool as Pool

        if self.n_jobs == -1:
            self.pool=Pool()
        else:
            self.pool=Pool(self.n_jobs)

    def choose_genetic_operator(self):
        """Normalizes operator probabilities so that values sum to 1.
        """
        return choice(
            [o[0] for o in self.operators],
            1,
            [o[1] for o in self.operators]
        )[0]

    def make_spawner(self, num_inputs, num_classes=None):
        """Creates a spawner object used to generate random code.
        """
        input_instrs=[PyshInputInstruction(i) for i in range(num_inputs)]
        all_atom_gens=self.atom_generators + input_instrs
        if not num_classes is None:
            vote_instrs=[PyshClassVoteInstruction(i + 1)
                                             for i in range(num_classes)]
            all_atom_gens=self.atom_generators + vote_instrs
        self.spawner=r.PushSpawner(all_atom_gens)

    def init_population(self):
        """Generate random population of Individuals with Push programs.
        """
        self.population=Population()
        for i in range(self.population_size):
            gn=self.spawner.random_plush_genome(self.initial_max_genome_size)
            new_ind=Individual(gn)
            self.population.append(new_ind)

    def print_monitor(self, generation):
        """TODO: Write method docstring
        """
        print('Generation:', generation,
              '| Lowest Error:', self.population.lowest_error(),
              '| Avg Error:', self.population.average_error(),
              '| Number of Unique Programs:', self.population.unique())

    def print_monitor_verbose(self, generation):
        """TODO: Write method docstring
        """
        print()
        print('Generation:', generation),
        print('| Lowest Error:', self.population.lowest_error()),
        print('| Avg Error:', self.population.average_error()),
        print('| Number of Unique Programs:', self.population.unique())

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
        return np.apply_along_axis(self.best_.run_program, 1, X)


class PushGPRegressor(BaseEstimator, PyshMixin):
    """A Scikit-learn estimator that uses PushGP for symbolic regression tasks.
    TODO: Write fit_metric docstring

    Attributes
    ----------

    best_ : Individual
        Best Individual present in the last generation of evolution.

    best_error_ : float
        Total error of the Individual stored in best_. This is considered the
        overall training error of the SymbolicRegressor.
    """

    def __init__(self, fit_metric=mean_squared_error, error_threshold=0,
        max_generations=1000, population_size=300,
        selection_method='epsilon_lexicase', n_jobs=1,
        operators=DEFAULT_GENETICS, initial_max_genome_size=50,
        program_growth_cap=100, atom_generators=REGRESSION_ATOM_GENERATORS,
        verbose=0, epsilon='auto', tournament_size=7, simplification_steps=500):

        PyshMixin.__init__(self, error_threshold=error_threshold,
            max_generations=max_generations, population_size=population_size,
            selection_method=selection_method, n_jobs=n_jobs,
            operators=operators, program_growth_cap=program_growth_cap,
            initial_max_genome_size=initial_max_genome_size,
            atom_generators=atom_generators, verbose=verbose,
            simplification_steps=simplification_steps, epsilon=epsilon,
            tournament_size=tournament_size)

        self.fit_metric=fit_metric

    def fit(self, X, y):
        """Fits the PushGPRegressor.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Target values.
        """

        def error_function(program):
            errors=[]
            for i in list(range(len(X))):
                interpr=PushInterpreter(inputs=X[i])
                interpr.run_push(program)
                result=interpr.state["_float"].ref(0)
                if type(result) == float:
                    errors.append(abs(result - y[i, 0]))
                else:
                    errors.append(99999)
            return errors

        n_feats=X.shape[1]
        self.make_spawner(n_feats)
        self.init_population()

        if hasattr(self, 'pool'):
            self.population.p_evaluate(error_function, self.pool)
        else:
            self.population.evaluate(error_function)

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
            next_gen=Population()
            for i in range(self.population_size):
                op=self.choose_genetic_operator()

                parents=[
                    self.population.select(self.selection_method, self.epsilon,
                                           self.tournament_size)
                    for p in range(op._num_parents)
                ]
                next_gen.append(op.produce(parents, self.spawner))
            self.population=next_gen

            # Evaluate population
            if hasattr(self, 'pool'):
                self.population.p_evaluate(error_function, self.pool)
            else:
                self.population.evaluate(error_function)

        self.best_error_ = min([i.total_error for i in self.population])
        test = lambda i: i.total_error == self.best_error_
        self.best_ = [i for i in self.population if test(i)][0]
        self.best_.simplify(error_function, self.simplification_steps,
                            self.verbose)
