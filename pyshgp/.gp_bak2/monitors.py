# _*_ coding: utf_8 _*_
"""
The :mod:`monitors` module defines various functions that gather simple
statistics about the evolutionary run. These can be used to monitor evolutionary
health.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

# Utility functions

def _get_all_total_errors(population):
    gnrtr = (ind.get_total_error() for ind in population)
    return np.fromiter(gnrtr, np.float)

def _get_all_genome_sizes(population):
    gnrtr = (len(ind.get_genome()) for ind in population)
    return np.fromiter(gnrtr, np.float)

def _get_population_error_matrix(population):
    return np.array([ind.get_errors() for ind in population])

def best_total_error(population):
    """
    :param list population: List of Individuals.
    :returns: Float of lowest total error in the population.
    """
    errs = _get_all_total_errors(population)
    return np.min(errs)

def average_total_error(population):
    """
    :param list population: List of Individuals.
    :returns: Float of average total error in the population.
    """
    errs = _get_all_total_errors(population)
    return np.around(np.sum(errs) / float(len(population)), 3)

def average_genome_size(population):
    """
    :param list population: List of Individuals.
    :returns: Float of average genome size in the population.
    """
    gnme_sizes = _get_all_genome_sizes(population)
    return np.around(np.sum(gnme_sizes) / float(len(population)), 3)

def smallest_genome_size(population):
    """
    :param list population: List of Individuals.
    :returns: Int of smallest genome size in the population.
    """
    gnme_sizes = _get_all_genome_sizes(population)
    return np.min(gnme_sizes)

def largest_genome_size(population):
    """
    :param list population: List of Individuals.
    :returns: Int of largest genome size in the population.
    """
    gnme_sizes = _get_all_genome_sizes(population)
    return np.max(gnme_sizes)

def unique_program_count(population):
    """
    :param list population: List of Individuals.
    :returns: Number of unique programs in population.
    """
    programs_set = {str(ind.get_program()) for ind in population}
    return len(programs_set)

def unique_error_vectors(population):
    """
    :param list population: List of Individuals.
    :returns: Number of unique error vectors.
    """
    error_mat = _get_population_error_matrix(population)
    return np.unique(error_mat).size

def best_by_total_error(population):
    """
    :param list population: List of Individuals.
    :returns: Best program in the population with respect to total error.
    """
    return sorted(population, key=lambda ind: ind.get_total_error())[0]

def lowest_error_on_each_case(population):
    """
    :param list population: List of Individuals.
    :returns: Vector of floats containing the lowest error in the population
    on each test cases.
    """
    error_mat = _get_population_error_matrix(population)
    return np.min(error_mat, axis = 0)

class Monitor:
    """Class that stores a montior function.
    """

    def __init__(self, name, function):
        self.name = name
        self.function = function

    def show(self, population):
        print(self.name, ':', self.function(population))

    # def save(self, filename='', database=False):
    #     pass
    
DEFAULT_MONITORS = [
    Monitor('Best total error', best_total_error),
    Monitor('Average total error', average_total_error),
    Monitor('Average genome size', average_genome_size),
    Monitor('Smallest genome size', smallest_genome_size),
    Monitor('Largest genome size', largest_genome_size),
    Monitor('Unique program count', unique_program_count),
    Monitor('Unique error vectors', unique_error_vectors),
    Monitor('Lowest error on each case', lowest_error_on_each_case),
    Monitor('Best program by total error', lambda p: best_by_total_error(p).get_program()),
    Monitor('Best program errors', lambda p: best_by_total_error(p).get_errors())
]
