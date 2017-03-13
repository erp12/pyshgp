# -*- coding: utf-8 -*-
"""
The :mod:`random` module defines various functions that produce random Plush
genomes and random Push programs.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random
import numpy.random as rand

from .. import utils as u
from .. import exceptions as e

from . import translation as t
from . import plush as pl

#################################
# random plush genome generator

close_probabilities = None
def random_closes(close_parens_probabilities):
    '''Returns a random number of closes based on close_parens_probabilities.

    close_parens_probabilities defaults to [0.772, 0.206, 0.021, 0.001]. 
    This is roughly equivalent to each selection coming from  a binomial
    distribution with n=4 and p=1/16.
    This results in the following probabilities:
    p(0) = 0.772
    p(1) = 0.206
    p(2) = 0.021
    p(3) = 0.001

    :param list close_parens_probabilities: List of probabilities that sum to 1.
    :returns: Integer between 0 and 3, inclusive. Denoted number of closes.
    '''
    prob = random.random()
    global close_probabilities
    if close_probabilities == None:
        close_probabilities = u.reductions(lambda i, j: i + j, close_parens_probabilities) + [1.0]
    parens = 0

    while prob > close_probabilities[1]:
        parens += 1
        del close_probabilities[0]
    return parens


def atom_to_plush_gene(atom, params):
    '''Converts an atom into a plush gene.

    :param [Anything] atom: The atom (instruction or literal) to convert to a gene.
    :param dict params: Relevant parameters. Generally, a dict of evolutionary parameters.
    :returns: Tuple representing Plush gene.
    '''
    instruction = None
    is_literal = False
    closes = None
    silent = None

    # Get list of epigenetic markers from 
    markers = params['epigenetic_markers'][:]
    markers.append('_instruction')

    # For each marker that is present
    for m in markers:
        if m == '_instruction':
            # The instruction marker.
            if callable(atom):
                # If it is callable, then it is likely a function that will produce a literal.
                fn_element = atom() 
                if callable(fn_element): # It's another function!
                    instruction = fn_element()
                else:
                    instruction = fn_element 
                is_literal = True
            else:
                # If atom is not callable, then it is the instruction/literal.
                # TODO: This *SHOULD* set is_literal to true if the atom is something like the number 7.
                instruction = atom
        elif m == '_close':
            # Returns a random number of close parens to follow the instruction in a program.
            closes = random_closes(params['close_parens_probabilities'])
        elif m == '_silent':
            # Determines if the gene should be marked as silent (will not appear in program)
            if random.random() > params['silent_instruction_probability']:
                silent = True
            else:
                silent = False
        else:
            raise e.UnkownEpigeneticMarker()
    # Create and return the gene tuple.
    return pl.make_plush_gene(instruction, is_literal, closes, silent)


def random_plush_instruction(params):
    '''Returns a random plush gene given atom_generators and epigenetic-markers.

    :param dict params: A dict of evolutionary parameters.
    :returns: A random Plush gene from the ``atom_generators``.
    '''
    atom = random.choice(list(params["atom_generators"]))
    return atom_to_plush_gene(atom, params)


def random_plush_genome_with_size(genome_size, params):
    '''Returns a random Plush genome with size ``genome_size``.
    
    :param int genome_size: The number of genes to be put in the Plush genome.
    :param dict params: A dict of evolutionary parameters.
    :returns: List of Plush genes (tuples). This is considered a genome.
    '''
    atoms = rand.choice(list(params["atom_generators"]), size=genome_size)
    return [atom_to_plush_gene(atom, params) for atom in atoms]


def random_plush_genome(max_genome_size, params):
    '''Returns a random Plush genome with size limited by max_genome_size.

    :param int max_genome_size: Max number of genes that could be in the genome.
    :param dict params: A dict of evolutionary parameters.
    :returns: List of Plush genes (tuples). This is considered a genome.
    '''
    genome_size = random.randint(1, max_genome_size)
    return random_plush_genome_with_size(genome_size, params)


#################################
# random push code generator


def random_push_code(max_points, params):
    '''Returns a random Push expression with size limited by max_points.

    :param int max_points: Max number of instructions, literals and parens.
    :param dict params: A dict of evolutionary parameters.
    :returns: A random Push program.
    '''
    max_genome_size = max(int(max_points /  2), 1)
    return t.translate_plush_genome_to_push_program(random_plush_genome(max_genome_size, params))
    