# _*_ coding: utf_8 _*_
"""
The :mod:`simplification` module contains functions that help when automatically
simplifying Push genomes and Push programs.

TODO: function parameter docstrings
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
    gn = copy(genome)
    genes_to_silence = randint(0, len(gn), n)
    for i in genes_to_silence:
        gn[i].is_silent = True
    return copy(gn)

def noop_n_random_genes(genome, n):
    """Returns a new genome that is identical to input genome, with n genes
    replaced with noop instructions.
    """
    gn = copy(genome)
    genes_to_silence = randint(0, len(gn), n)
    for i in genes_to_silence:
        gn[i].atom = copy(exec_noop_instruction)
    return copy(gn)

def simplify_once(genome):
    """Silences or noops between 1 and 3 random genes.
    """
    gn = deepcopy(genome)
    n = randint(1,4)
    action = choice(['silent', 'noop'])
    if action == 'silent':
        new_gn = silent_n_random_genes(gn, n)
    else:
        new_gn = noop_n_random_genes(gn, n)
    return copy(new_gn)
