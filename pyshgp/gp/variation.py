# _*_ coding: utf_8 _*_
"""
The :mod:`variation` module defines classes for variation operators (aka
genetic operators). These operators are used in evoluation to create new
children from selected parents.
"""

from abc import ABCMeta, abstractmethod
import random
import copy

from .population import Individual
from ..push import plush as pl
from ..utils import (
    perturb_with_gaussian_noise,
    gaussian_noise_factor,
    is_str_type,
    recognize_pysh_type
)


class VariationOperator(metaclass=ABCMeta):
    """The base class for all variation operators.

    Parameters
    ----------
    num_parents : int
        Number of parent Individuals the operator needs to produce a child
        Individual.
    """

    _num_parents = None

    def __init__(self, num_parents):
        self._num_parents = num_parents

    def check_num_parents(self, parents):
        if not len(parents) >= self._num_parents:
            msg = "{} parents passed to variation operator. Expected {}."
            raise ValueError(msg.format(len(parents), self._num_parents))

    @abstractmethod
    def produce(self, parents, spawner):
        """Produces a child.
        """


class VariationOperatorPipeline(VariationOperator):
    """Variation operator that chains together other variation operators.

    Parameters
    ----------
    operators : list of VariationOperators
        A list of operators to apply in order to produce the child Individual.
    """

    def __init__(self, operators):
        self.operators = operators
        needed_genomes = max([op._num_parents for op in self.operators])
        VariationOperator.__init__(self, needed_genomes)

    def produce(self, parents, spawner):
        """Produces a child using the VariationOperatorPipeline.

        Parameters
        ----------
        parents : list of Individuals
            A list of parents to use when producing the child.

        spawner : pyshgp.push.random.PushSpawner
            A spawner that can be used to create random Push code.
        """
        self.check_num_parents(parents)
        child = parents[0]
        for op in self.operators:
            child = op.produce([child] + list(parents[1:]), spawner)
        return child

##
#   Mutation
##


class PerturbCloseMutation(VariationOperator):
    """
    """

    def __init__(self, rate=0.01, standard_deviation=1):
        VariationOperator.__init__(self, 1)
        self.rate = rate
        self.standard_deviation = standard_deviation

    def produce(self, parents, spawner=None):
        """Produces a child by perturbing some floats in the parent.

        Parameters
        ----------
        parents : list of Individuals
            A list of parents to use when producing the child.

        spawner : pyshgp.push.random.PushSpawner
            A spawner that can be used to create random Push code.
        """
        self.check_num_parents(parents)
        new_genome = []
        for gene in parents[0].genome:
            if random.random() < self.rate:
                gene.closes = perturb_with_gaussian_noise(
                    self.standard_deviation,
                    gene.closes)
            new_genome.append(gene)
        return Individual(new_genome)


class PerturbIntegerMutation(VariationOperator):
    """
    """

    def __init__(self, rate=0.01, standard_deviation=1):
        VariationOperator.__init__(self, 1)
        self.rate = rate
        self.standard_deviation = standard_deviation

    def produce(self, parents, spawner=None):
        """Produces a child by perturbing some integers in the parent.

        Parameters
        ----------
        parents : list of Individuals
            A list of parents to use when producing the child.

        spawner : pyshgp.push.random.PushSpawner
            A spawner that can be used to create random Push code.
        """
        self.check_num_parents(parents)
        new_genome = []
        for gene in parents[0].genome:
            if gene.is_literal:
                atom = gene.atom
                if recognize_pysh_type(atom) == '_integer' and random.random() < self.rate:
                    gene.atom = int(
                        perturb_with_gaussian_noise(
                            self.standard_deviation,
                            atom
                        )
                    )
            new_genome.append(gene)
        return Individual(new_genome)


class PerturbFloatMutation(VariationOperator):
    """
    """

    def __init__(self, rate=0.01, standard_deviation=1):
        VariationOperator.__init__(self, 1)
        self.rate = rate
        self.standard_deviation = standard_deviation

    def produce(self, parents, spawner=None):
        """Produces a child by perturbing some floats in the parent.

        Parameters
        ----------
        parents : list of Individuals
            A list of parents to use when producing the child.

        spawner : pyshgp.push.random.PushSpawner
            A spawner that can be used to create random Push code.
        """
        self.check_num_parents(parents)
        new_genome = []
        for gene in parents[0].genome:
            if gene.is_literal:
                atom = gene.atom
                if recognize_pysh_type(atom) == '_float' and random.random() < self.rate:
                    gene.atom = perturb_with_gaussian_noise(self.standard_deviation, atom)
            new_genome.append(gene)
        return Individual(new_genome)


class TweakStringMutation(VariationOperator):
    """
    """

    def __init__(self, rate=0.01, char_tweak_rate=0.1):
        VariationOperator.__init__(self, 1)
        self.rate = rate
        self.char_tweak_rate = char_tweak_rate

    def string_tweak(self, s):
        """Tweaks a string.
        """
        new_s = ""
        for c in s:
            if random.random() < self.char_tweak_rate:
                new_s += random.choice(['\t', '\n'] +
                                       list(map(chr, range(32, 127))))
            else:
                new_s += c
        return new_s

    def produce(self, parents, spawner=None):
        """Produces a child by perturbing some floats in the parent.

        Parameters
        ----------
        parents : list of Individuals
            A list of parents to use when producing the child.

        spawner : pyshgp.push.random.PushSpawner
            A spawner that can be used to create random Push code.
        """
        self.check_num_parents(parents)
        new_genome = []
        for gene in parents[0].genome:
            if gene.is_literal:
                atom = gene.atom
                if (recognize_pysh_type(atom) == '_float') and (random.random() < self.rate):
                    gene.atom = self.string_tweak(atom)
            new_genome.append(gene)
        return Individual(new_genome)


class FlipBooleanMutation(VariationOperator):
    """
    """

    def __init__(self, rate=0.01):
        VariationOperator.__init__(self, 1)
        self.rate = rate

    def produce(self, parents, spawner=None):
        """Produces a child by perturbing some floats in the parent.

        Parameters
        ----------
        parents : list of Individuals
            A list of parents to use when producing the child.

        spawner : pyshgp.push.random.PushSpawner
            A spawner that can be used to create random Push code.
        """
        self.check_num_parents(parents)
        new_genome = []
        for gene in parents[0].genome:
            if gene.is_literal:
                atom = gene.atom
                if recognize_pysh_type(atom) == '_boolean' and random.random() < self.rate:
                    gene.atom = not atom
            new_genome.append(gene)
        return Individual(new_genome)


class RandomAdditionMutation(VariationOperator):
    """
    """

    def __init__(self, rate=0.01):
        VariationOperator.__init__(self, 1)
        self.rate = rate

    def produce(self, parents, spawner):
        """Produces a child by perturbing some floats in the parent.

        Parameters
        ----------
        parents : list of Individuals
            A list of parents to use when producing the child.

        spawner : pyshgp.push.random.PushSpawner
            A spawner that can be used to create random Push code.
        """
        self.check_num_parents(parents)
        new_genome = []
        for gene in parents[0].genome:
            if random.random() < self.rate:
                new_genome.append(spawner.random_plush_gene())
            new_genome.append(gene)
        return Individual(new_genome)


class RandomReplaceMutation(VariationOperator):
    """
    """

    def __init__(self, rate=0.01):
        VariationOperator.__init__(self, 1)
        self.rate = rate

    def produce(self, parents, spawner):
        """Produces a child by perturbing some floats in the parent.

        Parameters
        ----------
        parents : list of Individuals
            A list of parents to use when producing the child.

        spawner : pyshgp.push.random.PushSpawner
            A spawner that can be used to create random Push code.
        """
        self.check_num_parents(parents)
        new_genome = []
        for gene in parents[0].genome:
            if random.random() < self.rate:
                new_genome.append(spawner.random_plush_gene())
            else:
                new_genome.append(gene)
        return Individual(new_genome)


# #               # #
#   Recombination   #
# #               # #


class Alternation(VariationOperator):
    """Uniformly alternates between the two parents.

    More information can be found on the `this Push-Redux page
    <https://erp12.github.io/push-redux/pages/genetic_operators/index.html#recombination>`_.

    Parameters
    ----------
    rate : float, optional (default=0.01)
        The probablility of switching which parent program elements are being
        copied from. Must be 0 <= rate <= 1. Defaults to 0.1.

    alignment_deviation : int, optional (default=10)
        The standard deviation of how far alternation may jump between indices
        when switching between parents.
    """

    def __init__(self, rate=0.01, alignment_deviation=10):
        # Initialize as a recombination operator
        VariationOperator.__init__(self, 2)
        # Set attributes
        self.rate = rate
        self.alignment_deviation = alignment_deviation

    def produce(self, parents, spawner=None):
        """Produces a child using the UniformMutation operator.

        Parameters
        ----------
        parents : list of Individuals
            A list of parents to use when producing the child.

        spawner : pyshgp.push.random.PushSpawner, optional
            A spawner that can be used to create random Push code. Not used by
            this operator.
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


##
#   Other
##


class Genesis(VariationOperator):
    """
    """

    def __init__(self, max_genome_size):
        VariationOperator.__init__(self, 0)
        self.max_genome_size = max_genome_size

    def produce(self, parents, spawner):
        return Individual(spawner.random_plush_genome(self.max_genome_size))


class Reproduction(VariationOperator):
    """
    """

    def __init__(self):
        VariationOperator.__init__(self, 1)

    def produce(self, parents, spawner=None):
        return parents[0]
