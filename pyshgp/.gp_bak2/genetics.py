# _*_ coding: utf_8 _*_
"""
The :mod:`Genetics` module defines a factory of genetic operators.
"""
import random

from ..push import plush as pl

class VariationOperator:
    """TODO: Write me"""

    #:Number of genomes to expect as input.
    _num_input_genomes = None

    def __init__(self, num_input_genomes):
        self._num_input_genomes= num_input_genomes

    def __call__(self):
        """Calls the genetic operator.
        """
        raise NotImplementedError()

class MutationOperator(VariationOperator):
    """Genetic operator that modifies 1 genome."""
    def __init__(self):
        GeneticOperator.__init__(self, 1)

class RecombinationOperator(VariationOperator):
    """Genetic operator that combines 2 genomes."""
    def __init__(self):
        GeneticOperator.__init__(self, 2)

class GeneticOperatorPipeline(VariationOperator):
    """Genetic operator that chains together other genetic operators.
    """
    def __init__(self, operators):
        self.operators = operators

        needed_genomes = max([op.num_input_genomes for op in self.operators])
        GeneticOperator.__init__(self, needed_genomes)

    def __call__(self, *args):
        if not len(args) == self._num_input_genomes:
            raise Exception('Wrong number of parents provided to \
                             GeneticOperatorPipeline')

        genomes = args
        for op in self.operators:
            genomes[0] = op(*genomes[:op._num_input_genomes])

        return genomes[0]

##
#   Mutation
##

class UniformMutation(MutationOperator):
    """Uniformly mutates individual.

    For each token in program, there is *rate* probability of being mutated. If a token
    is to be mutated, it has a *constant_tweak_rate* probability of being mutated using
    a constant mutator (which varies depending on the type of the token), and
    otherwise is replaced with a random instruction.

    More information can be found on the `this Push-Redux page
    <https://erp12.github.io/push-redux/pages/genetic_operators/index.html#mutation>`_.
    """
        #: TODO: Write me!
        rate = None
        #: TODO: Write me!
        constant_tweak_rate = None
        #: TODO: Write me!
        float_standard_deviation = None
        #: TODO: Write me!
        int_standard_deviation  = None
        #: TODO: Write me!
        string_char_change_rate = None

    def __init__(self, rate=0.1, constant_tweak_rate=0.5,
        float_standard_deviation=1.0, int_standard_deviation=1,
        string_char_change_rate=0.1):
        # Initialize as a mutation operator
        MutationOperator.__init__(self)
        # Set attributes
        self.rate = rate
        self.constant_tweak_rate = constant_tweak_rate
        self.float_standard_deviation = float_standard_deviation
        self.int_standard_deviation = int_standard_deviation
        self.string_char_change_rate = string_char_change_rate

    def __call__(self, genome, random_push_generator):
        self.random_push_generator = random_push_generator
        new_genome = [self.token_mutator(gene) for gene in genome]
        return new_genome

    def string_tweak(self, s):
        new_s = ""
        for c in s:
            if random.random() < self.string_char_change_rate:
                new_s += random.choice(['\t', '\n'] + list(map(chr, range(32, 127))))
            else:
                new_s += c
        return new_s

    def constant_mutator(token):
        """Mutates a literal value depending on its type.
        """
        if token.is_literal:
            const = token.atom
            instr = None

            if type(const) == float:
                instr = u.perturb_with_gaussian_noise(self.float_standard_deviation, const)
            elif type(const) == int:
                instr = round(u.perturb_with_gaussian_noise(self.int_standard_deviation, const))
            elif type(const) == str:
                instr = self.string_tweak(const)
            elif type(const) == bool:
                instr = random.choice([True, False])
            return pl.(instr, True, token.closes, token.is_silent)
        else:
            return self.random_push_generator.random_plush_instruction()

    def token_mutator(token):
        if random.random() < self.rate:
            if random.random() < self.constant_tweak_rate:
                token = self.constant_mutator(token)
            else:
                token = self.random_push_generator.random_plush_instruction()
        return token


# def uniform_close_mutation(genome, evo_params):
#     """Uniformly mutates the ``_close`` markers in the individual's genome.
#
#     Each ``_close`` will have a ``uniform_close_mutation_rate`` probability of
#     being changed, and those that are changed have a ``close_increment_rate``
#     chance of being incremented, and are otherwise decremented.
#
#     More information can be found on the `this Push-Redux page
#     <https://erp12.github.io/push-redux/pages/genetic_operators/index.html#mutation>`_.
#
#     :param list genome: Plush genome to mutate.
#     :param dict evo_params: Parameters for evolution.
#     :returns: The new mutated genome.
#     """
#     if not "_close" in evo_params["epigenetic_markers"]:
#         return genome
#     return [close_mutator(gene, evo_params) for gene in genome]

##
#   Recombination
##

class Alternation(RecombinationOperator):
    """
    Uniformly alternates between the two parents.

    More information can be found on the `this Push-Redux page
    <https://erp12.github.io/push-redux/pages/genetic_operators/index.html#recombination>`_.
    """
    #: TODO: Write me
    rate = None
    #: TODO: Write me
    alignment_deviation = None

    def __init__(self, rate = 0.1, alignment_deviation = 10):
        self.rate = rate
        self.alignment_deviation = alignment_deviation

    def __call__(self, genome1, genome2):
        resulting_genome = []
        # Random pick which parent to start from
        use_parent_1 = random.choice([True, False])
        loop_times = len(parent_1)
        if not use_parent_1:
            loop_times = len(parent_2)
        i = 0
        while (i < loop_times) and (len(resulting_genome) < evo_params["max_points"]):
            if random.random() < evo_params["alternation_rate"]:
                # Switch which parent we are pulling genes from
                i += round(evo_params["alignment_deviation"] * u.gaussian_noise_factor())
                i = int(max(0, i))
                use_parent_1 = not use_parent_1
            else:
                # Pull gene from parent
                if use_parent_1:
                    resulting_genome.append(parent_1[i])
                else:
                    resulting_genome.append(parent_2[i])
                i = int(i+1)
            # Change loop stop condition
            loop_times = len(parent_1)
            if not use_parent_1:
                loop_times = len(parent_2)
        return resulting_genome
