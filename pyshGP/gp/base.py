# _*_ coding: utf_8 _*_
"""
The :mod:`base` module defines the basic classes used to perform GP with
``pyshgp``.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import gp
import params as p

from .. import utils as u
from .. import interpreter as interp
from ..push.instructions import registered_instructions as ri

from sklearn.base import BaseEstimator
from sklearn.metrics import mean_squared_error
import numpy as np

class PushGPEvolver:
    """Evolves push programs. Stores the solution for later use.
    """

    #: Error function used to evaluate individuals during evolution.
    error_function = None

    #: Evolutionary parameters used by the Evolver.
    params = p.default_evolutionary_params
    
    _best = None

    def __init__(self, error_function, **args):
        self.error_function = error_function
        self.params = u.merge_dicts(self.params, args)
        self.evolve()

    def evolve()
        best, is_solution = gp.evolution(self.error_function, self.params)
        self._best = best

    def run_best(*inputs):
        """Runs the best program found by evolution
        """
        interpreter = interp.PushInterpreter(*inputs)
        interpreter.run_push(self._best)
        return 

    def get_best_program()
        return _best.get_program()

    def get_training_error()
        return _best.get_total_error()


class PushGPRegressor(BaseEstimator):
    """A Scikit-learn estimator that uses PushGP for symbolic regression tasks.
    """

    _atom_generators = list(u.merge_sets(ri.get_instructions_by_pysh_type('_exec'),
                                         ri.get_instructions_by_pysh_type('_boolean'),
                                         ri.get_instructions_by_pysh_type('_integer'),
                                         ri.get_instructions_by_pysh_type('_float')
                                         [lambda: random.randint(0, 100),
                                          lambda: random.random()]))

    def __init__(error_metric = mean_squared_error,
                 population_size = 1000,
                 selection_method = 'epsilon-lexicase',
                 mutation_recombination_ratio = 0.5,
                 parallel_evaluation = True):
        self.error_metric = error_metric
        self.population_size = population_size
        self.selection_method = selection_method
        self.mutation_recombination_ratio = mutation_recombination_ratio
        self.parallel_evaluation = parallel_evaluation

