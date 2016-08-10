# _*_ coding: utf_8 _*_
"""
Created on 5/20/2016

@author: Eddie
"""
import random

from .. import pysh_random
from .. import pysh_globals as g
from .. import pysh_utils as u
from .. import pysh_simplification as simp
from .. import pysh_instruction as instr
from ..instructions import *
from ..instructions import registered_instructions 
from ..instructions import input_output

import individual as ind
import genetic_operators as go
import selection as sel
import evolution_monitors as monitor

default_evolutionary_params = {
"error_threshold" : 0, # If any total error of individual is below this, that is considered a solution
"population_size" : 300, # Size of the population at each generation
"max_generations" : 100, # Max generations before evoluion stops. Will stop sooner if solution is found
"max_genome_initial_size" : 50, # Maximum size of random genomes generated for initial population
"max_points" : 400, # Maximum size of push genomes and push programs, as counted by points in the program. <- Might not be implemented correctly yet

# The instructions that pushgp will use in random code generation
"atom_generators" : registered_instructions.registered_instructions + 
                    [lambda: random.randint(0, 100),
                     lambda: random.random()],

# Probabilities of parents from previous generation undergoing each
# genetic operators to produce a child.
# More coming soon!
"genetic_operator_probabilities" : {"alternation" : 0.7,
									"uniform_mutation" : 0.1},

#############
# SELECTION #
#############
"selection_method" : "lexicase", # Options are 'lexicase' or 'tournament';

# Arguments related to Tournament Selection
"tournament_size" : 7, # If using tournament selection, the size of the tournaments

###########################
# CROSSOVER & ALTERNATION #
###########################

# Arguments related to alternation
"alternation_rate" : 0.01, # When using alternation, how often alternates between the parents
"alignment_deviation" : 10, # When using alternation, the standard deviation of how far alternation may jump between indices when switching between parents

############
# MUTATION #
############

# Arguments related to uniform mutation
"uniform_mutation_rate" : 0.01, # The probability of each token being mutated during uniform mutation
"uniform_mutation_constant_tweak_rate" : 0.5, # The probability of using a constant mutation instead of simply replacing the token with a random instruction during uniform mutation
"uniform_mutation_float_gaussian_standard_deviation" : 1.0, # The standard deviation used when tweaking float constants with Gaussian noise
"uniform_mutation_int_gaussian_standard_deviation" : 1, # The standard deviation used when tweaking integer constants with Gaussian noise

# Epignenetics
"epigenetic_markers" : ["_close"], # A vector of the epigenetic markers that should be used in the individuals. Implemented options include: :close, :silent
"close_parens_probabilities" : [0.772, 0.206, 0.021, 0.001], # A vector of the probabilities for the number of parens ending at that position.         
"silent_instruction_probability" : 0.2, # If :silent is used as an epigenetic-marker, this is the probability of random instructions having :silent be true

# Program Simplification
"final_simplification_steps" : 10000, # The number of simplification steps that will happen upon finding a solution.

# Monitoring Evolution
"things_to_monitor" : {"best_total_error" : True,
					   "average_total_error" : True,
					   "average_genome_size" : True,
					   "smallest_genome_size" : True,
					   "largest_genome_size" : True,
					   "unique_genome_count" : False}
}



def load_program_from_list(lst, atom_generators = default_evolutionary_params["atom_generators"]):
	"""
	Loads a program from a list, and checks each string in list for an
	instruction with the same name.
	"""
	program = []
	for el in lst:
		if type(el) == int or type(el) == float or type(el) == bool:
			program.append(el)
		elif type(el) == str:
			matching_intstructions = filter(lambda x: x.name == el, registered_instructions.registered_instructions)
			if len(matching_intstructions) > 0:
				program.append(matching_intstructions[0])
			else:
				program.append(el)
		elif type(el) == list:
			program.append(load_program_from_list(el))
	return program

def evaluate_population(population, error_function):
	"""
	Updates the errors of the population.
	"""
	for ind in population:
		if ind.get_errors() == []:
			errors = error_function(ind.get_program())
			ind.set_errors(errors)


def evolution(error_function, problem_params):
	"""
	Basic evolutionary loop.
	"""
	print "Starting GP Run"

	#print evolutionary_params
	evolutionary_params = u.merge_dicts(default_evolutionary_params, problem_params)

	# Create Initial Population
	population = []
	for i in range(evolutionary_params["population_size"]):
		rand_genome = pysh_random.random_plush_genome(evolutionary_params)
		population.append(ind.Individual(rand_genome, evolutionary_params))

	
	# Evaluate initial population to get their error vectors
	evaluate_population(population, error_function)
	# Sort the population
	population = sorted(population, key=lambda ind: ind.get_total_error())

	for g in range(evolutionary_params["max_generations"]):
		print
		print "Starting Generation:", g

		# Select parents and mate them to create offspring
		print "Performing selection and variation."
		selction_func = sel.lexicase_selection
		if evolutionary_params["selection_method"] == "tournament":
			selection_func = sel.tournament_selection
		offspring = []
		for i in range(len(population)):
			parent_1 = selction_func(population, 1)[0]
			parent_2 = selction_func(population, 1)[0]
			if random.random() < evolutionary_params["genetic_operator_probabilities"]["alternation"]:
				offspring_genome = go.alternation(parent_1.get_genome(), parent_2.get_genome(), evolutionary_params)
				offspring.append(ind.Individual(offspring_genome, evolutionary_params))
				#print offspring[i].get_genome(), " :: ", parent_1.get_genome(), " :: ", parent_2.get_genome()
			else:
				offspring.append(random.choice([parent_1, parent_2]))
		# Apply mutation to the offspring
		for i in range(0, len(offspring)):
			if random.random() < evolutionary_params["genetic_operator_probabilities"]["uniform_mutation"]:
				new_offspring_genome = go.uniform_mutation(offspring[i].get_genome(), evolutionary_params)
				offspring[i].set_genome(new_offspring_genome)

		print "Evaluating new individuals in population."
		evaluate_population(offspring, error_function)
		print "Installing next generation."
		population = offspring
		population = sorted(population, key=lambda ind: ind.get_total_error())
		
		# Print things user wants to monitor
		monitor.print_monitors(population, evolutionary_params["things_to_monitor"])

		# Check for any solutions
		solutions = filter(lambda ind: ind.get_total_error() <= evolutionary_params["error_threshold"], population)
		if len(solutions) > 0:
			print "Solution Found:"
			print
			print "Program:"
			print solutions[0].get_program()
			print "Genome:"
			print solutions[0].get_genome()
			print 
			simp.auto_simplify(solutions[0], error_function, evolutionary_params["final_simplification_steps"])
			break # Finish evolutionary run

		if g == evolutionary_params['max_generations'] - 1:
			print 'Best program in final generation:'
			print population[0].get_program()
			print 'Errors:', population[0].get_errors()




