# _*_ coding: utf_8 _*_
"""
The :mod:`base` module defines the basic classes used to perform GP with
``pyshgp``.

TODO: Some way to validate that best and error_function are in sync, etc
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import random
import inspect
import numpy as np

from . import selection, genetics, monitors, reports
from .. import utils as u
from ..push import interpreter as interp
from ..push import instruction as instr
from ..push import random as rand
from ..push.instructions import registered_instructions as ri

from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.metrics import mean_squared_error, euclidean_distances


DEFAULT_GENETICS = [
    (genetics.Alternation(), 0.7),
    (genetics.UniformMutation(), 0.1),
    (genetics.GeneticOperatorPipeline(
        (genetics.Alternation(),
         genetics.UniformMutation()), 0.2)
]

class PyshMixin:
    """Contains all evoluationary
    """

    #:TODO: write docstring
    error_threshold=None
    #:TODO: write docstring
    max_generations=None
    #:TODO: write docstring
    population_size=None
    #:TODO: write docstring
    selector=None
    #:TODO: write docstring
    genetic_operators=None
    #:TODO: write docstring
    max_workers=None
    #:TODO: write docstring
    initial_max_genome_size=None
    #:TODO: write docstring
    max_genome_size=None

    def __init__(self, error_function, error_threshold=0, max_generations=1000,
            population_size=0, selector=selection.Selector(method='lexicase'),
            genetic_operators=DEFAULT_GENETICS, max_workers=-1,
            initial_max_genome_size=50, max_genome_size=200,
            spawner=rand.PushSpawner()):
        self.error_threshold=error_threshold
        self.max_generations=max_generations
        self.population_size=population_size
        self.selector=selector
        self.genetic_operators=genetic_operators
        self.max_workers=max_workers
        self.initial_max_genome_size=initial_max_genome_size
        self.max_genome_size=max_genome_size
        self.spwaner=spawner

        if not max_workers == 1:
            self.init_executor(max_workers)

        self.normalize_genetic_operator_probabilities()

    def init_executor(self, max_workers):
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

        if max_workers == -1:
            self.pool=Pool()
        else:
            self.pool=Pool(max_workers)

    def normalize_genetic_operator_probabilities(self):
        """Normalizes operator probabilities so that values sum to 1.
        """
        new_ops=[]
        tot=sum([go[1] for go in self.genetic_operators])
        for go in self.genetic_operators:
            new_prob=round(go[1] / tot, 4)
            new_ops.append(go[0], new_prob)
        self.genetic_operators=new_ops

    def generate_random_population(self):
        """Generate random population of Individuals with Push programs.

        :returns: A list of Individual objects with randomly generated genomes
        and translated programs.
        """
        population=[]
        for i in range(self.population_size):
            gn=self.spawner.random_plush_genome(self.initial_max_genome_size)
            new_ind=individual.Individual(gn)
            population.append(new_ind)
        return population

    def evaluate_individual(self, ind, error_function):
        """Adds an error vector to an individual evaluated on the given
        error_function.

        :param Individual ind: An instance of the Individual class.
        :param function error_function: Python function that evaluates an
        individual based on its program.
        :return: Individual with error values assigned.
        """
        if ind.get_errors() == []:  # Only evaluate the individual if it hasn't been already.
            errors = error_function(ind.get_program())
            ind.set_errors(errors)
        return ind

    def evaluate_population(self, population, error_function):
        """Updates the errors of the population.

        :param list population: List of Individual objects
        :param function error_function: Python function that evaluates an
        individual based on its program.
        :returns: New population (list of Individuals) with error values
        assigned.
        """
        if hasattr(self, 'pool'):
            # If parallel evalutation, map over the pool.
            return self.pool.map(self.evaluate_individual, population,
                [error_function] * len(population))
        else:
            # If serial evaluation
            return [self.evaluate_individual(ind, error_function) for ind in population]

    def simplify_individual(self, individual, error_function, steps=5000):
        """TODO
        """
        return simp.auto_simplify(individual.get_program,
                                  individual.get_total_error, error_function,
                                  steps)

    def
#

class SimplePyshEvolver(PyshMixin):
    """Simple evolutionary algorithm to perform PushGP.
    """

    #:TODO
    monitors=None
    #:TODO
    reports=None
    #:TODO
    status='initialized'

    _error_function=None
    _best=None

    def __init__(self, error_threshold=0, max_generations=1000,
            population_size=0, selection_method='lexicase',
            genetic_operators=DEFAULT_GENETICS, max_workers=-1,
            initial_max_genome_size=50, max_genome_size=200,
            spawner=rand.PushSpawner(),
            monitors=DEFAULT_MONITORS, reports=None):
        super(SimplePyshEvolver, self).__init__(error_threshold,
                max_generations, population_size, selector,genetic_operators,
                max_workers, initial_max_genome_size, max_genome_size, spawner)
        self.monitors = monitors

    def monitor_population(self, population):
        """TODO: Write method
        """
        pass

    def run_report(self, population):
        """TODO: Write method
        """
        pass


    def evolve(self, error_function, verbosity=0):
        """Evolves a program that minimizes the result output of error_function.
        """

        if verbosity > 1:
            print("=== Starting GP Run With Following Parameters ===")
            print("TODO: Actually print the Parameters")

        if verbosity > 1:
            print("Creating Initial Population")
        population=self.generate_random_population()




    def run_best(*inputs):
        """Runs the best program found by evolution
        """
        interpreter=interp.PushInterpreter(*inputs)
        interpreter.run_push(self._best)
        return

    def get_best_program():
        return _best.get_program()

    def get_training_error():
        return _best.get_total_error()

# class ESPyshEvolver(PyshMixin):
#     """Just and example of what else could be done with the PyshMixin.
#     """


class PushGPRegressor(BaseEstimator):
    """A Scikit-learn estimator that uses PushGP for symbolic regression tasks.
    """

    #: Instance of PushGPEvolver that evolves the _best_program.
    _evolver=None

    #: Atom generators that make sense to use for regression problems.
    _atom_generators=list(u.merge_sets(
        ri.get_instructions_by_pysh_type('_exec'),
        ri.get_instructions_by_pysh_type('_boolean'),
        ri.get_instructions_by_pysh_type('_integer'),
        ri.get_instructions_by_pysh_type('_float'),
        [lambda: random.randint(0, 100), lambda: random.random()]))

    def __init__(self,
                 error_metric=mean_squared_error,
                 population_size=1000,
                 max_generations=1000,
                 selection_method='epsilon_lexicase',
                 mutation_recombination_ratio=0.5,
                 alternation_rate=0.1,
                 uniform_mutation_rate=0.1,
                 max_workers=None,
                 final_simplification_steps=5000):
        args, _, _, values=inspect.getargvalues(inspect.currentframe())
        values.pop("self")
        for arg, val in values.items():
            setattr(self, arg, val)

    def _create_params_for_data(self, X):
        """Creates evolutionary param dict specific to the problem and data.
        """

        # Get the number of input features.
        try:
            num_inpts=X.shape[1]
        except IndexError:
            num_inpts=1

        # Gather the final list of atom generates based on the regression
        # related instructions and the number of inputs.
        atm_gnrtrs=self._atom_generators + \
            [instr.PyshInputInstruction(i) for i in np.arange(num_inpts)]

        # Build final set of evolutionary hyperparameters
        final_params=p.default_evolutionary_params
        for k in p.default_evolutionary_params.keys():
            try:
                new_val=getattr(self, k)
            except AttributeError:
                continue
            final_params[k]=new_val

        # Set other parameters
        final_params['genetic_operator_probabilities']={
            "alternation": 1 - self.mutation_recombination_ratio,
            "uniform_mutation": self.mutation_recombination_ratio
        }
        final_params['atom_generators']=atm_gnrtrs

        return final_params

    def _get_output(self, program, x):
        """ Runs a push program given a set of inputs.

        :param program: A push program.
        :param x: A list (or array) of input values.
        :returns: A float returned by the push program.
        """
        interpreter=interp.PushInterpreter(inputs=x)
        interpreter.run_push(program)
        return interpreter.state.stacks["_float"].ref(0)

    def fit(self, X, y):

        def _error(program):
            errors=[]
            for i in list(range(len(X))):
                output=self._get_output(program, [X[i]])
                if type(output) == float:
                    errors.append(self.error_metric([output], [y[i]]))
                else:
                    errors.append(99999)
            return errors

        final_params=self._create_params_for_data(X)
        _best_program=PushGPEvolver(_error, final_params)
        return self


class PushGPClassifier(BaseEstimator, ClassifierMixin):
    """A Scikit-learn estimator that uses PushGP for classification tasks.
    """

    #: Instance of PushGPEvolver that evolves the _best_program.
    _evolver=None

    #: Atom generators that make sense to use for regression problems.
    _atom_generators=list(u.merge_sets(
        ri.registered_instructions,
        [lambda: random.randint(0, 100), lambda: random.random()]))

    def __init__(self,
                 error_metric=euclidean_distances,
                 population_size=1000,
                 max_generations=1000,
                 selection_method='lexicase',
                 mutation_recombination_ratio=0.5,
                 alternation_rate=0.1,
                 uniform_mutation_rate=0.1,
                 max_workers=None,
                 final_simplification_steps=5000):
        args, _, _, values=inspect.getargvalues(inspect.currentframe())
        values.pop("self")
        for arg, val in values.items():
            setattr(self, arg, val)

    def _create_params_for_data(self, X, y):
        """Creates evolutionary param dict specific to the problem and data.
        """

        # Get the number of input features.
        try:
            num_inpts=X.shape[1]
        except IndexError:
            num_inpts=1

        # Gather the final list of atom generates based on the regression
        # related instructions and the number of inputs.
        atm_gnrtrs=self._atom_generators + \
            [instr.PyshInputInstruction(i) for i in np.arange(num_inpts)] + \
            [instr.PyshClassVoteInstruction(i + 1, '_integer') for i in np.arange(self._num_classes)] + \
            [instr.PyshClassVoteInstruction(i + 1, '_float')
                                            for i in np.arange(self._num_classes)]

        # Build final set of evolutionary hyperparameters
        final_params=p.default_evolutionary_params
        for k in p.default_evolutionary_params.keys():
            try:
                new_val=getattr(self, k)
                final_params[k]=new_val

            except AttributeError:
                continue

        # Set other parameters
        final_params['genetic_operator_probabilities']={
            "alternation": 1 - self.mutation_recombination_ratio,
            "uniform_mutation": self.mutation_recombination_ratio
        }
        final_params['atom_generators']=atm_gnrtrs

        return final_params

    def _get_output(self, program, x):
        """ Runs a push program given a set of inputs.

        :param program: A push program.
        :param x: A list (or array) of input values.
        :returns: A float returned by the push program.
        """
        interpreter=interp.PushInterpreter(inputs=x)
        for i in range(self._num_classes):
            interpreter.state.stacks["_output"].push_item(0)

        interpreter.run_push(program)
        votes=np.array(interpreter.state.stacks["_output"][1:])
        return int(np.argmax(votes))

    def fit(self, X, y):

        self._num_classes=len(np.unique(y))

        def _error(program):
            errors=np.array([])
            for i in list(range(len(X))):
                output=self._get_output(program, X[i])
                if type(output) == int:
                    errors=np.append(errors,
                                       (self.error_metric(np.array([output]).reshape(1, -1),
                                                          np.array([y[i]]).reshape(-1, 1))))
                else:
                   errors=np.append(errors, 99999)
            return errors

        final_params=self._create_params_for_data(X, y)
        self._evolver=PushGPEvolver(_error, final_params)
        return self
