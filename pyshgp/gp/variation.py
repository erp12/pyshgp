"""The :mod:`variation` module defines classes for variation operators.

Variation operators (aka genetic operators) are used in evolutionary/genetic
algorithms to create "child" genomes from "parent" genomes.

"""
from abc import ABC, abstractmethod
from typing import Sequence, Union
import math

from numpy.random import random, choice

from pyshgp.push.types import PushType
from pyshgp.push.atoms import Literal
from pyshgp.gp.genome import Genome, GeneSpawner
from pyshgp.tap import tap
from pyshgp.utils import DiscreteProbDistrib, instantiate_using


class VariationOperator(ABC):
    """Base class of all VariationOperators.

    Parameters
    ----------
    num_parents : int
        Number of parent Genomes the operator needs to produce a child
        Individual.

    Attributes
    ----------
    num_parents : int
        Number of parent Genomes the operator needs to produce a child
        Individual.

    """

    def __init__(self, num_parents: int):
        self.num_parents = num_parents

    def checknum_parents(self, parents: Sequence[Genome]):
        """Raise error if given too few parents.

        Parameters
        ----------
        parents
            A list of parent Genomes given to the operator.

        """
        if not len(parents) >= self.num_parents:
            raise ValueError("Variation operator given {a} parents. Expected {e}.".format(
                a=len(parents),
                e=self.num_parents)
            )

    @tap
    @abstractmethod
    def produce(self, parents: Sequence[Genome], spawner: GeneSpawner) -> Genome:
        """Produce a child Genome from parent Genomes and optional GenomeSpawner.

        Parameters
        ----------
        parents
            A list of parent Genomes given to the operator.
        spawner
            A GeneSpawner that can be used to produce new genes (aka Atoms).

        """
        pass


class VariationStrategy(DiscreteProbDistrib):
    """A collection of VariationOperator and how frequently to use them."""

    def add(self, op: VariationOperator, p: float):
        """Add an element with a relative probability.

        Parameters
        ----------
        op : VariationOperator
            The VariationOperator to add to the variation strategy.
        p : float
            The probability of using the given operator relative to the other
            operators that have been added to the VariationStrategy.

        """
        super().add(op, p)


class VariationPipeline(VariationOperator):
    """Variation operator that sequentially applies multiple others variation operators.

    Parameters
    ----------
    operators : Sequence[VariationOperators]
        A list of operators to apply in order to produce the child Genome.

    Attributes
    ----------
    operators : Sequence[VariationOperators]
        A list of operators to apply in order to produce the child Genome.
    num_parents : int
        Number of parent Genomes the operator needs to produce a child
        Individual.

    """

    def __init__(self, operators: Sequence[VariationOperator]):
        num_parents_needed = max([op.num_parents for op in operators])
        super().__init__(num_parents_needed)
        self.operators = operators

    @tap
    def produce(self, parents: Sequence[Genome], spawner: GeneSpawner) -> Genome:
        """Produce a child Genome from parent Genomes and optional GenomeSpawner.

        Parameters
        ----------
        parents
            A list of parent Genomes given to the operator.
        spawner
            A GeneSpawner that can be used to produce new genes (aka Atoms).

        """
        super().produce(parents, spawner)
        self.checknum_parents(parents)
        child = parents[0]
        for op in self.operators:
            child = op.produce([child] + parents[1:], spawner)
        return child


# Utilities

def _gaussian_noise_factor():
    """Return Gaussian noise of mean 0, std dev 1.

    Returns
    --------
    Float samples from Gaussian distribution.

    Examples
    --------
    >>> gaussian_noise_factor()
    1.43412557975
    >>> gaussian_noise_factor()
    -0.0410900866765

    """
    return math.sqrt(-2.0 * math.log(random())) * math.cos(2.0 * math.pi * random())


# Mutations

# @TODO: Implement all the common literal mutations.
class LiteralMutation(VariationOperator, ABC):
    """Base class for mutations of literal Atoms.

    Parameters
    ----------
    push_type : pyshgp.push.types.PushType
        The PushType which the operator can mutate.
    rate : float
        The probability of applying the mutation to a given Literal.

    Attributes
    ----------
    push_type : pyshgp.push.types.PushType
        The PushType which the operator can mutate.
    rate : float
        The probability of applying the mutation to a given Literal.
    num_parents : int
        Number of parent Genomes the operator needs to produce a child
        Individual.

    """

    def __init__(self, push_type: PushType, rate: float = 0.01):
        super().__init__(1)
        self.rate = rate
        self.push_type = push_type

    @abstractmethod
    def _mutate_literal(self, literal: Literal) -> Literal:
        ...

    @tap
    def produce(self, parents: Sequence[Genome], spawner: GeneSpawner = None) -> Genome:
        """Produce a child Genome from parent Genomes and optional GenomeSpawner.

        Parameters
        ----------
        parents
            A list of parent Genomes given to the operator.
        spawner
            A GeneSpawner that can be used to produce new genes (aka Atoms).

        """
        super().produce(parents, spawner)
        self.checknum_parents(parents)
        new_genome = Genome()
        for atom in parents[0]:
            if isinstance(atom, Literal) and self.push_type == atom.push_type and random() < self.rate:
                new_atom = self._mutate_literal(atom)
            else:
                new_atom = atom
            new_genome = new_genome.append(new_atom)
        return new_genome


class DeletionMutation(VariationOperator):
    """Uniformly randomly removes some Atoms from parent.

    Parameters
    ----------
    rate : float
        The probability of removing any given Atom in the parent Genome.
        Default is 0.01.

    Attributes
    ----------
    rate : float
        The probability of removing any given Atom in the parent Genome.
        Default is 0.01.
    num_parents : int
        Number of parent Genomes the operator needs to produce a child
        Individual.

    """

    def __init__(self, deletion_rate: float = 0.01):
        super().__init__(1)
        self.rate = deletion_rate

    @tap
    def produce(self, parents: Sequence[Genome], spawner: GeneSpawner) -> Genome:
        """Produce a child Genome from parent Genomes and optional GenomeSpawner.

        Parameters
        ----------
        parents
            A list of parent Genomes given to the operator.
        spawner
            A GeneSpawner that can be used to produce new genes (aka Atoms).

        """
        super().produce(parents, spawner)
        self.checknum_parents(parents)
        new_genome = Genome()
        for gene in parents[0]:
            if random() < self.rate:
                continue
            new_genome = new_genome.append(gene)
        return new_genome


class AdditionMutation(VariationOperator):
    """Uniformly randomly adds some Atoms to parent.

    Parameters
    ----------
    rate : float
        The probability of adding a new Atom at any given point in the parent
        Genome. Default is 0.01.

    Attributes
    ----------
    rate : float
        The probability of adding a new Atom at any given point in the parent
        Genome. Default is 0.01.
    num_parents : int
        Number of parent Genomes the operator needs to produce a child
        Individual.

    """

    def __init__(self, addition_rate: float = 0.01):
        super().__init__(1)
        self.rate = addition_rate

    @tap
    def produce(self, parents: Sequence[Genome], spawner: GeneSpawner) -> Genome:
        """Produce a child Genome from parent Genomes and optional GenomeSpawner.

        Parameters
        ----------
        parents
            A list of parent Genomes given to the operator.
        spawner
            A GeneSpawner that can be used to produce new genes (aka Atoms).

        """
        super().produce(parents, spawner)
        self.checknum_parents(parents)
        new_genome = Genome()
        for gene in parents[0]:
            if random() < self.rate:
                new_genome = new_genome.append(spawner.random_gene())
            new_genome = new_genome.append(gene)
        return new_genome


# Recombinations

class Alternation(VariationOperator):
    """Uniformly alternates between the two parent genomes.

    Parameters
    ----------
    rate : float, optional (default=0.01)
        The probability of switching which parent program elements are being
        copied from. Must be 0 <= rate <= 1. Defaults to 0.1.
    alignment_deviation : int, optional (default=10)
        The standard deviation of how far alternation may jump between indices
        when switching between parents.

    Attributes
    ----------
    rate : float, optional (default=0.01)
        The probability of switching which parent program elements are being
        copied from. Must be 0 <= rate <= 1. Defaults to 0.1.
    alignment_deviation : int, optional (default=10)
        The standard deviation of how far alternation may jump between indices
        when switching between parents.
    num_parents : int
        Number of parent Genomes the operator needs to produce a child
        Individual.

    """

    def __init__(self, alternation_rate=0.01, alignment_deviation=10):
        super().__init__(2)
        self.rate = alternation_rate
        self.alignment_deviation = alignment_deviation

    @tap
    def produce(self, parents: Sequence[Genome], spawner: GeneSpawner = None) -> Genome:
        """Produce a child Genome from parent Genomes and optional GenomeSpawner.

        Parameters
        ----------
        parents
            A list of parent Genomes given to the operator.
        spawner
            A GeneSpawner that can be used to produce new genes (aka Atoms).

        """
        super().produce(parents, spawner)
        self.checknum_parents(parents)
        gn1 = parents[0]
        gn2 = parents[1]
        new_genome = Genome()
        # Random pick which parent to start from
        use_parent_1 = choice([True, False])
        loop_times = len(gn1)
        if not use_parent_1:
            loop_times = len(gn2)
        i = 0
        while (i < loop_times):
            if random() < self.rate:
                # Switch which parent we are pulling genes from
                i += round(self.alignment_deviation * _gaussian_noise_factor())
                i = int(max(0, i))
                use_parent_1 = not use_parent_1
            else:
                # Pull gene from parent
                if use_parent_1:
                    new_genome = new_genome.append(gn1[i])
                else:
                    new_genome = new_genome.append(gn2[i])
                i = int(i + 1)
            # Change loop stop condition
            loop_times = len(gn1)
            if not use_parent_1:
                loop_times = len(gn2)
        return new_genome


# Other

class Genesis(VariationOperator):
    """Creates an entirely new (and random) genome.

    Parameters
    ----------
    size
        The child genome will contain this many Atoms if size is an integer.
        If size is a pair of integers, the genome will be of a random
        size in the range of the two integers.

    Attributes
    ----------
    size
        The child genome will contain this many Atoms if size is an integer.
        If size is a pair of integers, the genome will be of a random
        size in the range of the two integers.
    num_parents : int
        Number of parent Genomes the operator needs to produce a child
        Individual.

    """

    def __init__(self, *, size: Union[int, Sequence[int]]):
        super().__init__(0)
        self.size = size

    @tap
    def produce(self, parents: Sequence[Genome], spawner: GeneSpawner) -> Genome:
        """Produce a child Genome from parent Genomes and optional GenomeSpawner.

        Parameters
        ----------
        parents
            A list of parent Genomes given to the operator.
        spawner
            A GeneSpawner that can be used to produce new genes (aka Atoms).

        """
        super().produce(parents, spawner)
        return spawner.spawn_genome(self.size)


class Cloning(VariationOperator):
    """Clones the parent genome.

    Attributes
    ----------
    num_parents : int
        Number of parent Genomes the operator needs to produce a child
        Individual.

    """

    def __init__(self):
        super().__init__(1)

    @tap
    def produce(self, parents: Sequence[Genome], spawner: GeneSpawner = None) -> Genome:
        """Produce a child Genome from parent Genomes and optional GenomeSpawner.

        Parameters
        ----------
        parents
            A list of parent Genomes given to the operator.
        spawner
            A GeneSpawner that can be used to produce new genes (aka Atoms).

        """
        super().produce(parents, spawner)
        return parents[0]


def get_variation_operator(name: str, **kwargs) -> VariationOperator:
    """Get the variaton operator class with the given name."""
    name_to_cls = {
        "deletion": DeletionMutation,
        "addition": AdditionMutation,
        "alternation": Alternation,
        "genesis": Genesis,
        "cloning": Cloning,
        # UMAD citation: https://dl.acm.org/citation.cfm?id=3205455.3205603
        "umad": VariationPipeline([AdditionMutation(0.09), DeletionMutation(0.0826)]),
        "umad-shrink": VariationPipeline([AdditionMutation(0.09), DeletionMutation(0.1)]),
        "umad-grow": VariationPipeline([AdditionMutation(0.09), DeletionMutation(0.0652)])
    }
    op = name_to_cls.get(name, None)
    if op is None:
        raise ValueError("No varition operator '{nm}'. Supported names: {lst}.".format(
            nm=name,
            lst=list(name_to_cls.keys())
        ))
    if isinstance(op, type):
        op = instantiate_using(op, kwargs)
    return op
