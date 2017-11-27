# -*- coding: utf-8 -*-
"""
The :mod:`random` module defines classes that produce random Plush
genomes and random Push programs.

TODO: There should be better structure here in terms of what goes in the
spawner class and what is a global function.
"""
import random
import numpy.random as rand

from ..utils import reductions
from .translation import genome_to_program
from .plush import Gene
from .instruction import Instruction


_DEFAULT_CLOSE_PROBABILITIES = [0.772, 0.206, 0.021, 0.001]


class Spawner:
    """Spawns new push programs and plush genomes.

    Parameters
    ----------
    atom_generators : list
        List of atoms, and functions that produce atoms, to choose from when
        generating random code.
    close_parens_probabilities : list (optional)
        List of probabilities that sum to one. Recomended you leave this as
        the default.
    """

    def __init__(self, atom_generators, close_parens_probabilities='default'):
        self.atom_generators = atom_generators
        if close_parens_probabilities == 'default':
            self.close_parens_probabilities = _DEFAULT_CLOSE_PROBABILITIES[:]
        else:
            self.close_parens_probabilities = close_parens_probabilities

    def random_closes(self):
        """Returns a random number of closes based on close_parens_probabilities.

        close_parens_probabilities defaults to [0.772, 0.206, 0.021, 0.001].
        This is roughly equivalent to each selection coming from  a binomial
        distribution with n=4 and p=1/16.
        This results in the following probabilities:
        p(0) = 0.772
        p(1) = 0.206
        p(2) = 0.021
        p(3) = 0.001

        Returns
        --------
         Integer between 0 and 3, inclusive. Denoted number of closes.
        """
        prob = random.random()
        close_probabilities = reductions(
            lambda i, j: i + j,
            self.close_parens_probabilities
        ) + [1.0]
        parens = 0

        while prob > close_probabilities[1]:
            parens += 1
            del close_probabilities[0]
        return parens

    def atom_to_plush_gene(self, atom):
        """Converts an atom into a plush gene.

        Parameters
        ----------
        atom : Instruction or literal
            The atom (instruction or literal) to convert to a gene.

        Returns
        --------
            Instance of Gene.
        """
        is_literal = False
        proc_atom = None
        if callable(atom):
            # If it is callable, then it is likely a function that will
            # produce a literal.
            fn_element = atom()
            if callable(fn_element):  # It's another function!
                proc_atom = fn_element()
            else:
                proc_atom = fn_element
            is_literal = True
        else:
            # If atom is not callable, then it is the instruction/literal.
            proc_atom = atom
            is_literal = not isinstance(proc_atom, Instruction)

        return Gene(proc_atom, is_literal, self.random_closes())

    def random_plush_gene(self):
        """Returns a random plush gene given atom_generators and
        epigenetic-markers.

        Returns
        --------
            A random Plush gene from the ``atom_generators``.
        """
        atom = random.choice(list(self.atom_generators))
        return self.atom_to_plush_gene(atom)

    def random_plush_genome_with_size(self, genome_size):
        """Returns a random Plush genome with size ``genome_size``.

        Parameters
        ----------
        genome_size : int
            The number of genes to be put in the Plush genome.

        Returns
        --------
            List of Plush genes. This is considered a genome.
        """
        atoms = rand.choice(list(self.atom_generators), size=genome_size)
        return [self.atom_to_plush_gene(atom) for atom in atoms]

    def random_plush_genome(self, max_genome_size):
        """Returns a random Plush genome with size limited by max_genome_size.

        Parameters
        ----------
        max_genome_size : int
            Max number of genes that could be in the genome.

        Returns
        --------
            List of Plush genes (tuples). This is considered a genome.
        """
        genome_size = random.randint(1, max_genome_size)
        return self.random_plush_genome_with_size(genome_size)

    def random_push_code(self, max_points):
        """Returns a random Push expression with size limited by max_points.

        Parameters
        ----------
        max_points : int
            Max number of instructions, literals and parens.

        Returns
        --------
             A random Push program.
        """
        max_genome_size = max(int(max_points / 2), 1)
        genome = self.random_plush_genome(max_genome_size)
        return genome_to_program(genome)
