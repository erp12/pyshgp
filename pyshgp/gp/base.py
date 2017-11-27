"""
TODO: Module docstg
"""
from numpy.random import choice
from random import random, randint

from pathos.multiprocessing import ProcessingPool as Pool

from .population import Population, Individual
from .variation import (
    VariationOperatorPipeline,
    UniformMutation,
    PerturbCloseMutation,
    Alternation
)
from ..push import random as r
from ..push.registered_instructions import (
    instruction_set,
    get_instructions_by_pysh_type
)
from ..push.instruction import InputInstruction
from ..utils import merge_sets


_alternation = Alternation()
_mutation = UniformMutation()
DEFAULT_GENETICS = [
    (_alternation, 0.2),
    (_mutation, 0.2),
    (PerturbCloseMutation(rate=0.1), 0.1),
    (VariationOperatorPipeline((_alternation, _mutation)), 0.5)
]
DEFAULT_ATOM_GENERATORS = list(merge_sets(
    instruction_set.values(),
    [lambda: randint(0, 100), lambda: random()])
)
REGRESSION_ATOM_GENERATORS = list(merge_sets(
    get_instructions_by_pysh_type('_exec'),
    get_instructions_by_pysh_type('_float'),
    [lambda: randint(0, 100), lambda: random()])
)
CLASSIFICATION_ATOM_GENERATORS = list(merge_sets(
    get_instructions_by_pysh_type('_exec'),
    get_instructions_by_pysh_type('_boolean'),
    get_instructions_by_pysh_type('_integer'),
    get_instructions_by_pysh_type('_float'),
    [lambda: randint(0, 100), lambda: random()])
)


class PyshBase:
    """Base class for all PushGP evolvers.

    TODO: Add validation checks.

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
    """

    def __init__(self, atom_generators='default', operators='default',
                 error_threshold=0, max_generations=1000, population_size=300,
                 selection_method='lexicase', n_jobs=1,
                 initial_max_genome_size=50, program_growth_cap=100,
                 verbose=0, epsilon='auto', tournament_size=7,
                 simplification_steps=2000):
        self.error_threshold = error_threshold
        self.max_generations = max_generations
        self.population_size = population_size
        self.selection_method = selection_method
        self.n_jobs = n_jobs
        self.operators = operators
        self.initial_max_genome_size = initial_max_genome_size
        self.program_growth_cap = program_growth_cap
        self.atom_generators = atom_generators
        self.verbose = verbose
        self.epsilon = epsilon
        self.tournament_size = tournament_size,
        self.simplification_steps = simplification_steps

        if not self.n_jobs == 1:
            self.init_executor()

        if atom_generators == 'default':
            self.atom_generators = DEFAULT_ATOM_GENERATORS

        if operators == 'default':
            self.operators = DEFAULT_GENETICS

    def init_executor(self):
        """Initializes a pool of processes.

        This requires pathos.multiprocessing because the standard
        multiprocessing library does not support pickling lambda and non-top
        level functions. Pathos specifically makes use of the dill package.

        .. TODO::
            TODO: If there is away around using pathos, it would be great to remove
            this dependency.
        """
        if self.n_jobs == 1:
            return

        if self.n_jobs == -1:
            self.pool = Pool()
        else:
            self.pool = Pool(self.n_jobs)

    def choose_genetic_operator(self):
        """Normalizes operator probabilities so that values sum to 1.
        """
        return choice(
            [o[0] for o in self.operators],
            1,
            [o[1] for o in self.operators]
        )[0]

    def make_spawner(self, num_inputs):
        """Creates a spawner object used to generate random code.

        Parameters
        ----------
        num_inputs : int
            The number of inputs instructions to generate at add to the Spawner.
            This should be set to the number of input values (features) that
            will be supplied to Push programs during evaluation.

        output_types : list
            A list of pysh types. The spawner will include instructions which
            ouput a list of outputs with the corresponding type in each index.
        """
        # Add input instructions.
        input_instrs = [InputInstruction(i) for i in range(num_inputs)]
        all_atom_gens = self.atom_generators + input_instrs
        # Create spawner
        self.spawner = r.PushSpawner(all_atom_gens)
        if self.verbose > 1:
            print('Creating Spawner with following atom generators:')
            print(self.spawner.atom_generators)

    def init_population(self):
        """Generate random population of Individuals with Push programs.
        """
        self.population = Population()
        for i in range(self.population_size):
            gn = self.spawner.random_plush_genome(self.initial_max_genome_size)
            new_ind = Individual(gn)
            self.population.append(new_ind)

    def print_monitor(self, generation):
        """Prints a basic set of values that can be used to manually monitor
        run health.

        TODO: Add validation check for if population exists.

        Parameters
        ----------
        generation : int
            The generation number.
        """
        print('Generation:', generation,
              '| Lowest Error:', self.population.lowest_error(),
              '| Avg Error:', self.population.average_error(),
              '| Number of Unique Programs:', self.population.unique())

    def print_monitor_verbose(self, generation):
        """Prints all implemented values that can be used to manually monitor
        run health.

        TODO: Add validation check for if population exists.

        Parameters
        ----------
        generation : int
            The generation number.
        """
        print()
        print('Generation', generation),
        print('Lowest Error:', self.population.lowest_error()),
        print('Avg Error:', self.population.average_error()),
        print('Number of Unique Programs:', self.population.unique())
        print('Best Program:', self.population.best_program())
        print('Errors of Best:', self.population.best_program_error_vector())


class PyshEstimatorMixin:
    """A Mixin class for the Sklearn estimators included in pyshgp.
    """

    def evolve(self, X, y):
        """Main evolutionary loop for the sklearn estimators in pyshgp.

        Parameters
        ----------
        X : {array-like, sparse matrix}, shape = (n_samples, n_features)
            Samples.

        y : {array-like, sparse matrix}, shape = (n_samples, 1)
            Target values.
        """
        self.init_population()
        self._evaluation(X, y)

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
                    self.population.select(self.selection_method, self.epsilon,
                                           self.tournament_size)
                    for p in range(op._num_parents)
                ]
                next_gen.append(op.produce(parents, self.spawner))
            self.population = next_gen

            # Evaluate population
            self._evaluation(X, y)

        self.best_error_ = min([i.total_error for i in self.population])

        def test(i): return i.total_error == self.best_error_
        self.best_ = [i for i in self.population if test(i)][0]
        self._simplification(X, y)
        return self
