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
    genes_to_silence = randint(0, len(genome), n)
    for i in genes_to_silence:
        genome[i].is_silent = True

def noop_n_random_genes(genome, n):
    """Returns a new genome that is identical to input genome, with n genes
    replaced with noop instructions.
    """
    genes_to_silence = randint(0, len(genome), n)
    for i in genes_to_silence:
        genome[i].atom = copy(exec_noop_instruction)

def simplify_once(genome):
    """Silences or noops between 1 and 3 random genes.
    """
    gn = deepcopy(genome)
    n = randint(1,4)
    action = choice(['silent', 'noop'])
    if action == 'silent':
        silent_n_random_genes(gn, n)
    else:
        noop_n_random_genes(gn, n)
    return gn
