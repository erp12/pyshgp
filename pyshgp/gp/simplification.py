# _*_ coding: utf_8 _*_
"""
The :mod:`simplification` module contains functions that help when automatically
simplifying Push genomes and Push programs.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
from numpy.random import random, randint, choice
from copy import copy, deepcopy

from ..push.instructions.code import exec_noop_instruction
from .. import utils as u

def silent_n_random_genes(genome, n):
    """Returns a new genome that is identical to input genome, with n genes
    marked as silent.
    """
    gn = deepcopy(genome)
    genes_to_silence = randint(0, len(gn), n)
    for i in genes_to_silence:
        gn[i].is_silent = True
    return gn

def noop_n_random_genes(genome, n):
    """Returns a new genome that is identical to input genome, with n genes
    replaced with noop instructions.
    """
    gn = deepcopy(genome)
    genes_to_silence = randint(0, len(gn), n)
    for i in genes_to_silence:
        gn[i].atom = copy(exec_noop_instruction)
    return gn

def simplify_once(individual):
    """Silences or noops between 1 and 3 random genes.
    """
    if len(individual.genome) == 0:
        return
    # Perform the potential simplification.
    n = randint(1,4)
    action = choice(['silent', 'noop'])
    if action == 'silent':
        individual.genome = silent_n_random_genes(individual.genome, n)
    else:
        individual.genome = noop_n_random_genes(individual.genome, n)
