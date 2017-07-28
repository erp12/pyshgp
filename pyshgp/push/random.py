# -*- coding: utf-8 -*-
"""
The :mod:`random` module defines classes that produce random Plush
genomes and random Push programs.

TODO: There should be better structure here in terms of what goes in the
spawner class and what is a global function.
"""
import random
import numpy.random as rand

from .. import utils as u
from .. import exceptions as e

from . import translation as t
from . import plush as pl


class PushSpawner:
    """
    Parameters
    ----------
    atom_generators : list
        List of atoms, and functions that produce atoms, to choose from when
        generating random code.
    epigenetic_markers : list
        TODO: Remove epigenetic_markers.
    close_parens_probabilities : int
        TODO: Refactor use of close_parens_probabilities.
    silent_gene_probability : float
        TODO: Remove epigenetic_markers.
    """

    def __init__(self, atom_generators,
                 epigenetic_markers=['_instruction', '_close'],
                 close_parens_probabilities=[0.772, 0.206, 0.021, 0.001],
                 silent_gene_probability=0.2):
        self.atom_generators = atom_generators
        self.close_parens_probabilities = close_parens_probabilities
        self.silent_gene_probability = silent_gene_probability
        self.epigenetic_markers = epigenetic_markers
        if '_instruction' not in self.epigenetic_markers:
            self.epigenetic_markers.appen('_instrucion')

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
        close_probabilities = u.reductions(
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
        instruction = None
        is_literal = False
        closes = None
        silent = False

        # For each marker that is present
        for m in self.epigenetic_markers:
            if m == '_instruction':
                # The instruction marker.
                if callable(atom):
                    # If it is callable, then it is likely a function that will
                    # produce a literal.
                    fn_element = atom()
                    if callable(fn_element):  # It's another function!
                        instruction = fn_element()
                    else:
                        instruction = fn_element
                    is_literal = True
                else:
                    # If atom is not callable, then it is the
                    # instruction/literal.
                    # TODO: This *SHOULD* set is_literal to true if the atom is
                    # something like the number 7.
                    instruction = atom
            elif m == '_close':
                # Returns a random number of close parens to follow the
                # instruction in a program.
                closes = self.random_closes()
            elif m == '_silent':
                # Determines if the gene should be marked as silent (will not
                # appear in program)
                silent = random.random() > self.silent_gene_probability
            else:
                raise e.UnkownEpigeneticMarker(m)
        # Create and return the gene tuple.
        return pl.Gene(instruction, is_literal, closes, silent)

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
        return t.genome_to_program(genome)
