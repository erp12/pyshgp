# _*_ coding: utf_8 _*_
"""
Created on 5/20/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import datetime
import random
import warnings
from collections import defaultdict

from .. import pysh_random
from .. import pysh_globals
from .. import utils as u
from .. import simplification as simp
from .. import instruction as instr
from ..instructions import boolean, char, code, common, numbers, string, input_output
from ..instructions import registered_instructions 

from . import individual
from . import genetic_operators as go
from . import evolution_monitors as monitor
from . import reporting


default_evolutionary_params = {
"error_threshold" : 0, # If any total error of individual is below this, that is considered a solution
"population_size" : 1000, # Size of the population at each generation
"max_generations" : 1000, # Max generations before evoluion stops. Will stop sooner if solution is found
"max_genome_initial_size" : 50, # Maximum size of random genomes generated for initial population
"max_points" : 200, # Maximum size of push genomes and push programs, as counted by points in the program. <- Might not be implemented correctly yet

# The instructions that pushgp will use in random code generation
"atom_generators" : u.merge_dicts(registered_instructions.registered_instructions,
                                  {"f1" : lambda: random.randint(0, 100),
                                   "f2" : lambda: random.random()}),

# Probabilities of parents from previous generation undergoing each
# genetic operators to produce a child.
# More coming soon!
"genetic_operator_probabilities" : {"alternation" : 0.7,
                                    "uniform_mutation" : 0.1,
                                    "alternation & uniform_mutation" : 0.2,
                                    "uniform_close_mutation" : 0.0},

#############
# SELECTION #
#############
"selection_method" : "lexicase", # Options are 'lexicase', 'epsilon_lexicase' or tournament';

# Arguments related to lexicase selection, and its variants
"epsilon_lexicase_epsilon" : None, # Defines a hard-coded epsilon. If None, automaticly defines epsilon using MAD.

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
"uniform_mutation_string_char_change_rate" : 0.1,

# Arguments related to uniform close mutation
"uniform_close_mutation_rate" : 0.1, # The probability of each :close being incremented or decremented during uniform close mutation.
"close_increment_rate" : 0.2, # The probability of making an increment change to :close during uniform close mutation, as opposed to a decrement change.

# Epignenetics
"epigenetic_markers" : ["_close"], # A vector of the epigenetic markers that should be used in the individuals. Implemented options include: :close, :silent
"close_parens_probabilities" : [0.772, 0.206, 0.021, 0.001], # A vector of the probabilities for the number of parens ending at that position.         
"silent_instruction_probability" : 0.2, # If :silent is used as an epigenetic-marker, this is the probability of random instructions having :silent be true

# Program Simplification
"final_simplification_steps" : 5000, # The number of simplification steps that will happen upon finding a solution.

# Monitoring Evolution
"things_to_monitor" : {"best_total_error" : True,
                       "average_total_error" : True,
                       "average_genome_size" : True,
                       "smallest_genome_size" : True,
                       "largest_genome_size" : True,
                       "unique_program_count" : True,
                       "unique_error_vectors" : True,
                       "best_program_by_total_error" : True},

# End of run plots
"reports" : {"timings" : True,
             "plot_piano_roll" : False},

#
"max_workers" : None, # If 1, pysh runs in single thread. Otherwise, pysh runs in parrell. If None, uses number of cores on machine.
"parallel_evaluation" : True,
"parallel_genetics" : False
}

def grab_command_line_params(evolutionary_params):
    '''
    Loads parameters from command line and overwrites the problem specific / default
    parameter values.
    '''
    for arg in sys.argv:
        if arg.startswith('--'):
            (param,val) = arg.split("=")
            if not (param[2:] in evolutionary_params):
                print("WARNING:", "Unknown evolutionary parameter", param[2:], ". Still added to parameters.")
            val = u.safe_cast_arg(val)
            evolutionary_params[param[2:]] = val

def init_executor(params):
    from pathos.multiprocessing import ProcessingPool as Pool

    if params["max_workers"] == None:
        params["pool"] = Pool()
    else:
        params['pool'] = Pool(params["max_workers"])


def load_program_from_list(lst, atom_generators = default_evolutionary_params["atom_generators"]):
    """
    Loads a program from a list, and checks each string in list for an
    instruction with the same name.
    """
    program = []
    for el in lst:
        if type(el) == int or type(el) == float or type(el) == bool or type(el) == pysh_globals.Character:
            program.append(el)
        elif (sys.version_info[0] == 3 and (type(el) is str or type(el) is bytes)) or (sys.version_info[0] == 2 and (type(el) is str or type(el) is unicode)):
            el = str(el)
            if el[:6] == "_input":
                inpt_num = int(el[6:])
                program.append(instr.Pysh_Input_Instruction("_input" + str(inpt_num)))
            else:
                matching_intstructions = [registered_instructions.registered_instructions[x] for x in registered_instructions.registered_instructions.keys() if x == el[1:]]
                if len(matching_intstructions) > 0:
                    program.append(matching_intstructions[0])
                else:
                    program.append(el)
        elif type(el) == list:
            program.append(load_program_from_list(el))
    return program

def generate_random_population(evolutionary_params):
    population = []
    for i in range(evolutionary_params["population_size"]):
        rand_genome = pysh_random.random_plush_genome(evolutionary_params)
        population.append(individual.Individual(rand_genome, evolutionary_params))
    return population

def evaluate_individual(ind, error_function):
    if ind.get_errors() == []:
        errors = error_function(ind.get_program())
        reporting.total_errors_in_evalutaion_order.append(sum(errors))
        ind.set_errors(errors)
    return ind


def evaluate_population(population, error_function, evolutionary_params):
    """
    Updates the errors of the population.
    """
    if evolutionary_params['parallel_evaluation'] and (evolutionary_params["max_workers"] == None or evolutionary_params["max_workers"] > 1):
        # pathos.multiprocessing
        pool = evolutionary_params['pool']
        return pool.map(evaluate_individual, population, [error_function]*len(population))
    else:
        return list(map(evaluate_individual, population, [error_function]*len(population)))

def evolution(error_function, problem_params):
    """
    Basic evolutionary loop.
    """ 

    # Get the params for the run
    evolutionary_params = u.merge_dicts(default_evolutionary_params, problem_params)
    grab_command_line_params(evolutionary_params)
    evolutionary_params['genetic_operator_probabilities'] = u.normalize_genetic_operator_probabilities(evolutionary_params['genetic_operator_probabilities'])

    # Make certain params globally accesable
    pysh_globals.global_max_points = evolutionary_params['max_points']

    # Prepare for multi-threading if specified by user
    if evolutionary_params["max_workers"] == None or evolutionary_params["max_workers"] > 1:
        print("Preparing Pysh for parellel evaluations")
        init_executor(evolutionary_params)

    print("Starting GP Run With Parameters:")
    print()
    # Print the params for the run
    for key,value in evolutionary_params.items():
        print(key, end = ": ")
        if key == "atom_generators":
            print(list(value.keys()))
        else:
            print(value)
    print()

    # Create Initial Population
    print("Creating Initial Population")
    population = generate_random_population(evolutionary_params)
    
    # Evaluate initial population to get their error vectors
    print("Evaluating Initial Population")
    start_time = datetime.datetime.now()
    population = evaluate_population(population, error_function, evolutionary_params)
    end_time = datetime.datetime.now()
    reporting.log_timings("evaluation", start_time, end_time)

    # Sort the population
    population = sorted(population, key=lambda ind: ind.get_total_error())

    for g in range(evolutionary_params["max_generations"]):
        print()
        print("Starting Generation:", g)

        # Select parents and mate them to create offspring
        print("Performing selection and variation.")
        start_time = datetime.datetime.now()
        offspring = go.genetics(population, evolutionary_params)
        end_time = datetime.datetime.now()
        reporting.log_timings("genetics", start_time, end_time)

        print("Evaluating new individuals in population.")
        start_time = datetime.datetime.now()
        offspring = evaluate_population(offspring, error_function, evolutionary_params)
        end_time = datetime.datetime.now()
        reporting.log_timings("evaluation", start_time, end_time)
        
        print("Installing next generation.")
        population = offspring
        population = sorted(population, key=lambda ind: ind.get_total_error())
        
        # Print things user wants to monitor
        monitor.print_monitors(population, evolutionary_params["things_to_monitor"])

        # Check for any solutions
        solutions = [ind for ind in population if ind.get_total_error() <= evolutionary_params["error_threshold"]]
        if len(solutions) > 0:
            print()
            print("Solution Found:")
            print("Program:")
            print(solutions[0].get_program())
            print("Genome:")
            print(solutions[0].get_genome())
            print()
            simp.auto_simplify(solutions[0], error_function, evolutionary_params["final_simplification_steps"])
            break # Finish evolutionary run

        if g == evolutionary_params['max_generations'] - 1:
            print('Best program in final generation:')
            print(population[0].get_program())
            print('Errors:', population[0].get_errors())

    print()
    print("Generating End of Run Reports")
    if evolutionary_params["reports"]["timings"]:
        reporting.print_timings()
    print()
    if evolutionary_params["reports"]["plot_piano_roll"]:
        reporting.plot_piano_roll()

