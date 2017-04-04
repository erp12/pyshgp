# _*_ coding: utf_8 _*_
"""
The :mod:`base` module defines the basic classes used to perform GP with
``pyshgp``.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import random, inspect
import numpy as np

from . import gp
from . import params as p
from .. import utils as u
from ..push import interpreter as interp
from ..push import instruction as instr
from ..push.instructions import registered_instructions as ri

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import mean_squared_error, euclidean_distances


class PushGPEvolver:
    """Evolves push programs. Stores the solution for later use.
    """

    #: Error function used to evaluate individuals during evolution.
    error_function = None

    #: Evolutionary parameters used by the Evolver.
    _params = p.default_evolutionary_params
    
    _best = None

    def __init__(self, error_function, args):
        self.error_function = error_function
        self._params = u.merge_dicts(self._params, args)
        self.evolve()

    def evolve(self):
        best, is_solution = gp.evolution(self.error_function, self._params)
        self._best = best

    def run_best(*inputs):
        """Runs the best program found by evolution
        """
        interpreter = interp.PushInterpreter(*inputs)
        interpreter.run_push(self._best)
        return 

    def get_best_program():
        return _best.get_program()

    def get_training_error():
        return _best.get_total_error()


class PushGPRegressor(BaseEstimator):
    """A Scikit-learn estimator that uses PushGP for symbolic regression tasks.
    """

    #: Best program found by evolution. Used to make predictions.
    _best_program = None

    #: Atom generators that make sense to use for regression problems.
    _atom_generators = list(u.merge_sets(
        ri.get_instructions_by_pysh_type('_exec'),
        ri.get_instructions_by_pysh_type('_boolean'),
        ri.get_instructions_by_pysh_type('_integer'),
        ri.get_instructions_by_pysh_type('_float'),
        [lambda: random.randint(0, 100), lambda: random.random()]))

    def __init__(self,
                 error_metric = mean_squared_error,
                 population_size = 1000,
                 max_generations = 1000,
                 selection_method = 'epsilon_lexicase',
                 mutation_recombination_ratio = 0.5,
                 alternation_rate = 0.1,
                 uniform_mutation_rate = 0.1,
                 max_workers = None,
                 final_simplification_steps = 5000):
        args, _, _, values = inspect.getargvalues(inspect.currentframe())
        values.pop("self")
        for arg, val in values.items():
            setattr(self, arg, val)

    def _create_params_for_data(self, X):
        """Creates evolutionary param dict specific to the problem and data.
        """

        # Get the number of input features.
        try:
            num_inpts = X.shape[1]
        except IndexError:
            num_inpts = 1

        # Gather the final list of atom generates based on the regression
        # related instructions and the number of inputs.
        atm_gnrtrs = self._atom_generators + [instr.PyshInputInstruction(i) for i in np.arange(num_inpts)]

        # Build final set of evolutionary hyperparameters
        final_params = p.default_evolutionary_params
        for k in p.default_evolutionary_params.keys():
            try:
                new_val = getattr(self, k)
            except AttributeError:
                continue
            final_params[k] = new_val

        # Set other parameters
        final_params['genetic_operator_probabilities'] = {
            "alternation" : 1 - self.mutation_recombination_ratio,
            "uniform_mutation" : self.mutation_recombination_ratio
        }
        final_params['atom_generators'] = atm_gnrtrs

        return final_params

    def _get_output(self, program, x):
        """ Runs a push program given a set of inputs.

        :param program: A push program.
        :param x: A list (or array) of input values.
        :returns: A float returned by the push program.
        """
        interpreter = interp.PushInterpreter(inputs=x)
        interpreter.run_push(program)
        return interpreter.state.stacks["_float"].ref(0)

    def fit(self, X, y):

        def _error(program):
            errors = []
            for i in list(range(len(X))):
                output = self._get_output(program, [X[i]])
                if type(output) == float:
                    errors.append(self.error_metric([output], [y[i]]))
                else:
                    errors.append(99999)
            return errors

        final_params = self._create_params_for_data(X)
        _best_program = PushGPEvolver(_error, final_params)
        return self


class PushGPClassifier(BaseEstimator, ClassifierMixin):
    """A Scikit-learn estimator that uses PushGP for classification tasks.
    """

    #: Best program found by evolution. Used to make predictions.
    _best_program = None

    #: Atom generators that make sense to use for regression problems.
    _atom_generators = list(u.merge_sets(
        ri.registered_instructions,
        [lambda: random.randint(0, 100), lambda: random.random()]))

    def __init__(self,
                 error_metric = euclidean_distances,
                 population_size = 1000,
                 max_generations = 1000,
                 selection_method = 'lexicase',
                 mutation_recombination_ratio = 0.5,
                 alternation_rate = 0.1,
                 uniform_mutation_rate = 0.1,
                 max_workers = None,
                 final_simplification_steps = 5000):
        args, _, _, values = inspect.getargvalues(inspect.currentframe())
        values.pop("self")
        for arg, val in values.items():
            setattr(self, arg, val)

    def _create_params_for_data(self, X, y):
        """Creates evolutionary param dict specific to the problem and data.
        """

        # Get the number of input features.
        try:
            num_inpts = X.shape[1]
        except IndexError:
            num_inpts = 1

        # Gather the final list of atom generates based on the regression
        # related instructions and the number of inputs.
        atm_gnrtrs = self._atom_generators + \
            [instr.PyshInputInstruction(i) for i in np.arange(num_inpts)] + \
            [instr.PyshClassVoteInstruction(i+1, '_integer') for i in np.arange(self._num_classes)] + \
            [instr.PyshClassVoteInstruction(i+1, '_float') for i in np.arange(self._num_classes)]

        # Build final set of evolutionary hyperparameters
        final_params = p.default_evolutionary_params
        for k in p.default_evolutionary_params.keys():
            try:
                new_val = getattr(self, k)
            except AttributeError:
                continue
            final_params[k] = new_val

        # Set other parameters
        final_params['genetic_operator_probabilities'] = {
            "alternation" : 1 - self.mutation_recombination_ratio,
            "uniform_mutation" : self.mutation_recombination_ratio
        }
        final_params['atom_generators'] = atm_gnrtrs

        return final_params

    def _get_output(self, program, x):
        """ Runs a push program given a set of inputs.

        :param program: A push program.
        :param x: A list (or array) of input values.
        :returns: A float returned by the push program.
        """
        interpreter = interp.PushInterpreter(inputs=x)
        for i in range(self._num_classes):
            interpreter.state.stacks["_output"].push_item(0)

        interpreter.run_push(program)
        votes = np.array(interpreter.state.stacks["_output"][1:])
        return np.argmax(votes)

    def fit(self, X, y):

        self._num_classes = len(np.unique(y))

        def _error(program):
            errors = []
            for i in list(range(len(X))):
                output = self._get_output(program, X[i])
                if type(output) == int:
                    errors.append(self.error_metric([output], [y[i]]))
                else:
                    errors.append(99999)
            return errors

        final_params = self._create_params_for_data(X, y)
        _best_program = PushGPEvolver(_error, final_params)
        return self
