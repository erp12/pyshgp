# _*_ coding: utf_8 _*_
"""
The :mod:`variation` module defines classes for each genetic oper
"""
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import with_metaclass

from abc import ABCMeta, abstractmethod
import random
import copy

from .population import Individual
from ..push import plush as pl
from ..utils import perturb_with_gaussian_noise, gaussian_noise_factor


class VariationOperator(with_metaclass(ABCMeta)):
    """TODO: Write me
    """

    #:Number of genomes to expect as input. Needs to be set to be usable in a
    #:VariationOperatorPipeline
    _num_parents = None

    def __init__(self, num_parents):
        self._num_parents = num_parents

    def check_num_parents(self, parents):
        if not len(parents) >= self._num_parents:
            msg="{} parents passed to variation operator. Expected {}."
            raise ValueError(msg.format(len(parents), self._num_parents))

    @abstractmethod
    def produce(self, parents, spawner):
        """Produces a child.
        """

class VariationOperatorPipeline(VariationOperator):
    """Variation operator that chains together other variation operators.
    """

    def __init__(self, operators):
        self.operators = operators

        needed_genomes = max([op._num_parents for op in self.operators])
        VariationOperator.__init__(self, needed_genomes)

    def produce(self, parents, spawner):
        """TODO: Write method docstring.
        """
        self.check_num_parents(parents)
        child = parents[0]
        for op in self.operators:
            child = op.produce([child] + list(parents[1:]), spawner)
        return child

##
#   Mutation
##


class UniformMutation(VariationOperator):
    """Uniformly mutates individual.

    For each token in program, there is *rate* probability of being mutated. If a token
    is to be mutated, it has a *constant_tweak_rate* probability of being mutated using
    a constant mutator (which varies depending on the type of the token), and
    otherwise is replaced with a random instruction.

    More information can be found on the `this Push-Redux page
    <https://erp12.github.io/push-redux/pages/genetic_operators/index.html#mutation>`_.
    """
    #: The probablility of mutating any given gene of the individual's genome. Must
    #: be 0 <= rate <= 1. Defaults to 0.1.
    rate = None

    #: TODO: Write attribute docstring.
    constant_tweak_rate = None

    #: When float value is being perturbed with Gaussian noise, this is used as the
    #: standard deviation of the noise. Defaults to 1.0.
    float_standard_deviation = None

    #: When int value is being perturbed with Gaussian noise, this is used as the
    #: standard deviation of the noise. Defaults to 1.
    int_standard_deviation = None

    #: TODO: Write attribute docstring.
    string_char_change_rate = None

    def __init__(self, rate=0.1, constant_tweak_rate=0.5,
                 float_standard_deviation=1.0, int_standard_deviation=1,
                 string_char_change_rate=0.1):
        # Initialize as a mutation operator
        VariationOperator.__init__(self, 1)
        # Set attributes
        self.rate = rate
        self.constant_tweak_rate = constant_tweak_rate
        self.float_standard_deviation = float_standard_deviation
        self.int_standard_deviation = int_standard_deviation
        self.string_char_change_rate = string_char_change_rate

    def produce(self, parents, spawner):
        """TODO: Write method docstring.
        TODO: Re-write so that only constants get constant tweak.
        """
        self.check_num_parents(parents)
        self.spawner = spawner
        new_genome = []
        for gene in parents[0].genome:
            gene = copy.copy(gene)
            if random.random() < self.rate:
                if random.random() < self.constant_tweak_rate:
                    new_genome.append(self.constant_mutator(gene))
                else:
                    new_genome.append(self.spawner.random_plush_gene())
            else:
                new_genome.append(gene)
        return Individual(new_genome)

    def string_tweak(self, s):
        """TODO: Write method docstring.
        """
        new_s = ""
        for c in s:
            if random.random() < self.string_char_change_rate:
                new_s += random.choice(['\t', '\n'] +
                                       list(map(chr, range(32, 127))))
            else:
                new_s += c
        return new_s

    def constant_mutator(self, token):
        """Mutates a literal value depending on its type.
        TODO: Write method docstring.
        """
        if token.is_literal:
            const = token.atom
            atom = None

            if type(const) == float:
                atom = perturb_with_gaussian_noise(
                    self.float_standard_deviation, const)
            elif type(const) == int:
                atom = int(perturb_with_gaussian_noise(
                    self.int_standard_deviation, const))
            elif type(const) == str:
                atom = self.string_tweak(const)
            elif type(const) == bool:
                atom = random.choice([True, False])
            return pl.Gene(atom, True, token.closes, token.is_silent)
        else:
            return self.spawner.random_plush_gene()

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

class Alternation(VariationOperator):
    """Uniformly alternates between the two parents.

    More information can be found on the `this Push-Redux page
    <https://erp12.github.io/push-redux/pages/genetic_operators/index.html#recombination>`_.
    """
    #: The probablility of switching which parent program elements are being
    #: scopied from. Must be 0 <= rate <= 1. Defaults to 0.1.
    rate = None

    #: The standard deviation of how far alternation may jump between indices
    #: when switching between parents.
    alignment_deviation = None

    def __init__(self, rate=0.1, alignment_deviation=10,
                 max_genome_size=200):
        # Initialize as a recombination operator
        VariationOperator.__init__(self, 2)
        # Set attributes
        self.rate = rate
        self.alignment_deviation = alignment_deviation
        self.max_genome_size = max_genome_size

    def produce(self, parents, spawner=None):
        """TODO: Write method docstring
        """
        self.check_num_parents(parents)
        gn1 = parents[0].genome
        gn2 = parents[1].genome
        resulting_genome = []
        # Random pick which parent to start from
        use_parent_1 = random.choice([True, False])
        loop_times = len(gn1)
        if not use_parent_1:
            loop_times = len(gn2)
        i = 0
        while (i < loop_times):
            if random.random() < self.rate:
                # Switch which parent we are pulling genes from
                i += round(self.alignment_deviation * gaussian_noise_factor())
                i = int(max(0, i))
                use_parent_1 = not use_parent_1
            else:
                # Pull gene from parent
                if use_parent_1:
                    resulting_genome.append(gn1[i])
                else:
                    resulting_genome.append(gn2[i])
                i = int(i + 1)
            # Change loop stop condition
            loop_times = len(gn1)
            if not use_parent_1:
                loop_times = len(gn2)
        return Individual(resulting_genome)