# _*_ coding: utf_8 _*_
"""
The :mod:`simplification` module contains functions that help when
automatically simplifying Push genomes and Push programs.

TODO: function parameter docstrings
"""
from numpy.random import randint, choice
from copy import copy, deepcopy

from ..utils import count_points
from ..push.instructions.code import I_exec_noop
from .evaluate import (evaluate_with_function, evaluate_for_regression,
                       evaluate_for_classification)


def silent_n_random_genes(genome, n):
    """Returns a new genome that is identical to input genome, with n genes
    marked as silent.

    Parameters
    ----------
    genome : list of Genes
        List of Plush genes.

    n : int
        Number of gnese to switch to silent.
    """
    genes_to_silence = randint(0, len(genome), n)
    for i in genes_to_silence:
        genome[i].is_silent = True


def noop_n_random_genes(genome, n):
    """Returns a new genome that is identical to input genome, with n genes
    replaced with noop instructions.

    Parameters
    ----------
    genome : list of Genes
        List of Plush genes.

    n : int
        Number of gnese to switch to noop.
    """
    genes_to_silence = randint(0, len(genome), n)
    for i in genes_to_silence:
        genome[i].atom = copy(I_exec_noop)


def simplify_once(genome):
    """Silences or noops between 1 and 3 random genes.

    Parameters
    ----------
    genome : list of Genes
        List of Plush genes.
    """
    gn = deepcopy(genome)
    n = randint(1, 4)
    action = choice(['silent', 'noop'])
    if action == 'silent':
        silent_n_random_genes(gn, n)
    else:
        noop_n_random_genes(gn, n)
    return gn


def simplify_by_dataset(individual, X, y, mode, steps=1000, verbose=0):
    """Simplifies the genome (and program) of the individual based on
    a dataset by randomly removing some elements of the program and
    confirming that the total error remains the same or lower. This is
    acheived by silencing some genes in the individual's genome.

    Parameters
    ----------
    individual : Individual
        The individual to simply.

    X : {array-like, sparse matrix}, shape = (n_samples, n_features)
        Samples.

    y : {array-like, sparse matrix}, shape = (n_samples, 1)
        Labels.

    mode : str
        Valid options include "regression" and "classification"

    steps : int, optional (default=1000)
        Function to used to calculate the error of the individual. Sklearn
        scoring functions are supported.

    verbose :int, optional (default=0)
        When greater than 0, verbose printing is enabled.
    """
    # Print the origional size of the individual.
    if verbose > 0:
        print("Autosimplifying program of size:",
              count_points(individual.program))
    if mode == 'regression':
        evl = evaluate_for_regression
    elif mode == 'classification':
        evl = evaluate_for_classification
    for i in range(steps):
        # Evalaute the current individual and copy of the genome and error.
        individual = evl(individual, X, y)
        orig_err = copy(individual.total_error)
        orig_gn = copy(individual.genome)
        individual.genome = simplify_once(individual.genome)
        # Evaluate the individual again.
        individual = evl(individual, X, y)
        # Decide if the simplification impacted performance, and revert.
        if individual.total_error > orig_err:
            individual.genome = orig_gn
    # Print the final size of the individual.
    if verbose > 0:
        print("Finished simplifying program. New size:",
              count_points(individual.program))
        print(individual.program)
    return individual


def simplify_by_function(individual, error_function, steps=1000, verbose=0):
    """Simplifies the genome (and program) of the individual based on
    a function by randomly removing some elements of the program and
    confirming that the total error remains the same or lower. This is
    acheived by silencing some genes in the individual's genome.

    Parameters
    ----------
    individual : Individual
        The individual to simply.

    error_function : function
        Error function used to evaluate the individual's program.

    steps : int, optional (default=1000)
        Function to used to calculate the error of the individual. Sklearn
        scoring functions are supported.

    verbose :int, optional (default=0)
        When greater than 0, verbose printing is enabled.
    """
    # Print the origional size of the individual.
    if verbose > 0:
        print("Autosimplifying program of size:",
              count_points(individual.program))
    for i in range(steps):
        # Evalaute the current individual and copy of the genome and error.
        individual = evaluate_with_function(individual, error_function)
        orig_err = copy(individual.total_error)
        orig_gn = copy(individual.genome)
        individual.genome = simplify_once(individual.genome)
        # Evaluate the individual again.
        individual = evaluate_with_function(individual, error_function)
        # Decide if the simplification impacted performance, and revert.
        if individual.total_error > orig_err:
            individual.genome = orig_gn
    # Print the final size of the individual.
    if verbose > 0:
        print("Finished simplifying program. New size:",
              count_points(individual.program))
        print(individual.program)
    return individual
