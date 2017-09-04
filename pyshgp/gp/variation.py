# _*_ coding: utf_8 _*_
"""
The :mod:`variation` module defines classes for variation operators (aka
genetic operators). These operators are used in evoluation to create new
children from selected parents.
"""

from abc import ABCMeta, abstractmethod
import random

from .population import Individual
from ..utils import (
    perturb_with_gaussian_noise,
    gaussian_noise_factor,
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


class LiteralMutation(VariationOperator, metaclass=ABCMeta):
    """Base class for all constant mutators.
    """

    def __init__(self, pysh_type, rate=0.01):
        super().__init__(1)
        self.rate = rate
        self.pysh_type = pysh_type

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
            if gene.is_literal:
                lit = gene.atom
                if (recognize_pysh_type(lit) == self.pysh_type) and (random.random() < self.rate):
                    gene.atom = self._mutate_literal(lit)
            new_genome.append(gene)
        return Individual(new_genome)

    @abstractmethod
    def _mutate_literal(self, literal):
        """Mutates the literal.
        """

##
#   Mutation
##


class PerturbIntegerMutation(LiteralMutation):
    """Randomly perturbs the genes containing integer literals.
    """

    def __init__(self, rate=0.01, standard_deviation=1):
        super().__init__('_integer', rate)
        self.standard_deviation = standard_deviation

    def _mutate_literal(self, literal):
        """Mutates an interger literal.

        Parameters
        ----------
        literal : int
            An interger to perturb.

        Returns
        --------
        A perturbed interger.
        """
        return int(perturb_with_gaussian_noise(self.standard_deviation, literal))


class PerturbFloatMutation(LiteralMutation):
    """Randomly perturbs the genes containing float literals.
    """

    def __init__(self, rate=0.01, standard_deviation=1):
        super().__init__('_float', rate)
        self.standard_deviation = standard_deviation

    def _mutate_literal(self, literal):
        """Mutates a float literal.

        Parameters
        ----------
        literal : float
            An float to perturb.

        Returns
        --------
        A perturbed float.
        """
        return perturb_with_gaussian_noise(self.standard_deviation, literal)


class TweakStringMutation(LiteralMutation):
    """Randomly tweaks the string values in string literal genes.
    """

    def __init__(self, rate=0.01, char_tweak_rate=0.1):
        super().__init__('_string', rate)
        self.char_tweak_rate = char_tweak_rate

    def _mutate_literal(self, literal):
        """Mutates a string literal.

        Parameters
        ----------
        literal : str
            An string to tweak.

        Returns
        --------
        A tweaked string.
        """
        new_s = ""
        for c in literal:
            if random.random() < self.char_tweak_rate:
                new_s += random.choice(['\t', '\n'] + list(map(chr, range(32, 127))))
            else:
                new_s += c
        return new_s


class FlipBooleanMutation(LiteralMutation):
    """Randomly flips the boolean literal genes.
    """

    def __init__(self, rate=0.01):
        super().__init__('_boolean', rate)

    def _mutate_literal(self, literal):
        """Mutates a boolean literal.

        Parameters
        ----------
        literal : str
            An string to flip.

        Returns
        --------
        A flipped bool.
        """
        return not literal


class PerturbCloseMutation(VariationOperator):
    """Randomly perturbs the number of close markers on each gene.
    """

    def __init__(self, rate=0.01, standard_deviation=1):
        super().__init__(1)
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

        Returns
        --------
        A child Individual.
        """
        self.check_num_parents(parents)
        new_genome = []
        for gene in parents[0].genome:
            if random.random() < self.rate:
                gene.closes = int(
                    perturb_with_gaussian_noise(
                        self.standard_deviation,
                        gene.closes))
                if gene.closes < 0:
                    gene.closes = 0
            new_genome.append(gene)
        return Individual(new_genome)


class RandomDeletionMutation(VariationOperator):
    """Randomly removes some genes.
    """

    def __init__(self, rate=0.01):
        super().__init__(1)
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
                continue
            new_genome.append(gene)
        return Individual(new_genome)


class RandomAdditionMutation(VariationOperator):
    """Randomly adds new genes.
    """

    def __init__(self, rate=0.01):
        super().__init__(1)
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
    """Randomly replaces genes.
    """

    def __init__(self, rate=0.01):
        super().__init__(1)
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
        super().__init__(2)
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
    """Creates an entirely new (and random) genome.
    """

    def __init__(self, max_genome_size):
        VariationOperator.__init__(self, 0)
        self.max_genome_size = max_genome_size

    def produce(self, parents, spawner):
        return Individual(spawner.random_plush_genome(self.max_genome_size))


class Reproduction(VariationOperator):
    """Clones the parent genome.
    """

    def __init__(self):
        VariationOperator.__init__(self, 1)

    def produce(self, parents, spawner=None):
        return parents[0]
