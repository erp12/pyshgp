# _*_ coding: utf_8 _*_
"""
The :mod:`monitors` module defines various functions that gather simple 
statistics about the evolutionary run. These can be used to monitor evolutionary
health.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

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
    :returns: Float of lowest total error in the population.
    """
    errs = _get_all_total_errors(population)
    return np.around(np.sum(errs) / float(len(population)), 3)

def average_genome_size(population):
    """
    :param list population: List of Individuals.
    :returns: Float of lowest total error in the population.
    """
    gnme_sizes = _get_all_genome_sizes(population)
    return np.around(np.sum(gnme_sizes) / float(len(population)), 3)

def smallest_genome_size(population):
    """
    :param list population: List of Individuals.
    :returns: Float of lowest total error in the population.
    """
    gnme_sizes = _get_all_genome_sizes(population)
    return np.min(gnme_sizes)

def largest_genome_size(population):
    """
    :param list population: List of Individuals.
    :returns: Float of lowest total error in the population.
    """
    gnme_sizes = _get_all_genome_sizes(population)
    return np.max(gnme_sizes)

def unique_program_count(population):
    """
    :param list population: List of Individuals.
    :returns: Float of lowest total error in the population.
    """
    programs_set = {str(ind.get_program()) for ind in population}
    return len(programs_set)

def unique_error_vectors(population):
    """
    :param list population: List of Individuals.
    :returns: Float of lowest total error in the population.
    """
    error_mat = _get_population_error_matrix(population)
    return np.unique(error_mat).size

def best_by_total_error(population):
    """
    :param list population: List of Individuals.
    :returns: Float of lowest total error in the population.
    """
    return sorted(population, key=lambda ind: ind.get_total_error())[0]

def lowest_error_on_each_case(population):
    """
    :param list population: List of Individuals.
    :returns: Float of lowest total error in the population.
    """
    error_mat = _get_population_error_matrix(population)
    return np.min(error_mat, axis = 0)


def print_monitors(population, monitors_dict):
    """Prints all of the values the user asked to monitor in monitors_dict

    :params list population: List of Individuals.
    :params dict monitors_dict: Dictionary of which monitors to print.
    """
    if monitors_dict["best_total_error"]:
        print("Best Total Error:", best_total_error(population))
    if monitors_dict["average_total_error"]:
        print("Average Total Error:", average_total_error(population))
    if monitors_dict["average_genome_size"]:
        print("Average Genome Size:", average_genome_size(population))
    if monitors_dict["smallest_genome_size"]:
        print("Smallest Genome Size:", smallest_genome_size(population))
    if monitors_dict["largest_genome_size"]:
        print("Largest Genome Size:", largest_genome_size(population))
    if monitors_dict["unique_program_count"]:
        print("Number of Unique Programs:", unique_program_count(population), "/", len(population))
    if monitors_dict["unique_error_vectors"]:
        print("Number of Unique Error Vectors:", unique_error_vectors(population), "/", len(population))
    if monitors_dict["lowest_error_on_each_case"]:
        print("Best errors on each case:", lowest_error_on_each_case(population))
    if monitors_dict["best_by_total_error"]:
        i = best_by_total_error(population)
        print("Best program (by total error):")
        print(i.get_program())
        print("Error vector of best program (by total error):")
        print(i.get_errors())
