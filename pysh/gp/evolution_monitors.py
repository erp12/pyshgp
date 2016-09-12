# _*_ coding: utf_8 _*_
"""
Created on 5/25/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from .. import utils as u

def best_total_error(population):
	return sorted(population, key=lambda ind: ind.get_total_error())[0].get_total_error()

def average_total_error(population):
	return round(sum([ind.get_total_error() for ind in population]) / float(len(population)), 3)

def average_genome_size(population):
	return round(sum([len(ind.get_genome()) for ind in population]) / float(len(population)), 3)

def smallest_genome_size(population):
	return min([len(ind.get_genome()) for ind in population])

def largest_genome_size(population):
	return max([len(ind.get_genome()) for ind in population])

def unique_program_count(population):
	programs_set = {str(ind.get_program()) for ind in population}
	return len(programs_set)

def unique_error_vectors(population):
	error_vectors = [ind.get_errors() for ind in population]
	return len([list(x) for x in set(tuple(x) for x in error_vectors)])



def print_monitors(population, monitors_dict):
	'''
	Prints all of the values the user asked to monitor in monitors_dict
	'''
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