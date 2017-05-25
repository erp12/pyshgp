# _*_ coding: utf_8 _*_
"""
The :mod:`simplification` module defines method of automatically simplifying
Push genomes and Push programs.

.. todo::
    Genome simplification is very simplistic in its current state. This should
    be overhauled at some point to match the recent developments in
    simplification found in Clojush.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random
import copy

from .. import utils as u

from . import plush as pl


def auto_simplify(individual, error_function, steps, verbose=0):
    '''Simplifies the genome (and program) of the individual based on error_function.

    At each step, 1 or 2 random gene are silenced from the individual's genome.
    The genome is translated into a program which is then run through the
    error_funciton. If the errors of the program are equal or lower, the gene(s)
    remain silenced. Otherwise they are un-silenced.

    .. todo::
        Add bool to toggle printing.

    :param Individual individual: Individual to simplify (The genome, program,
    and error vector are needed.)
    :param function error_function: Error function.
    :param int steps: Number of simplification iterations.
    :returns: A new individual with a simplified program that performs the same.

    '''
    if verbose > 0:
        print("Autosimplifying program of size:",
              u.count_points(individual.program))

    for step in range(steps):

        # If individual's program has become empty, break.
        if individual.program == []:
            break;

        old_genome = copy.deepcopy(individual.genome)
        individual.evaluate(error_function)
        initial_error_vector = individual.error_vector[:]
        # Pick the index of the gene you want to silence
        genes_to_silence = [random.randint(0, len(individual.genome) - 1)]
        # Possibly silence another gene
        if random.random() < 0.5:
            genes_to_silence.append(random.randint(0, len(individual.genome) - 1))

        # Silence the gene(s)
        new_genome = copy.copy(individual.genome)
        for i in genes_to_silence:
            if not new_genome[i].is_silent:
                new_genome[i].is_silent = True

        # Make sure the program still performs the same
        individual.genome = new_genome
        new_error = error_function(individual.program)

        # reset genes if no improvment was made
        if not new_error <= initial_error_vector:
            individual.genome = old_genome

    if verbose > 0:
        print("Finished simplifying program. New size:",
              u.count_points(individual.program))
        print(individual.program)
    return individual
