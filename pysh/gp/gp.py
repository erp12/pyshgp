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
from . import evo_params

from sklearn.cluster import KMeans
import numpy as np


def load_program_from_list(lst, atom_generators = evo_params.default_evolutionary_params["atom_generators"]):
    """
    Loads a program from a list, and checks each string in list for an
    instruction with the same name.
    """
    program = []
    for el in lst:
        if type(el) == int or type(el) == float or type(el) == bool or type(el) == pysh_globals.Character:
            program.append(el)
        elif type(el) == instr.Pysh_Instruction or type(el) == instr.Pysh_Input_Instruction or type(el) == instr.Pysh_Class_Instruction:
            program.append(el)
        elif (sys.version_info[0] == 3 and (type(el) is str or type(el) is bytes)) or (sys.version_info[0] == 2 and (type(el) is str or type(el) is unicode)):
            el = str(el)
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
    evolutionary_params = u.merge_dicts(evo_params.default_evolutionary_params, problem_params)
    evo_params.grab_command_line_params(evolutionary_params)
    evolutionary_params['genetic_operator_probabilities'] = u.normalize_genetic_operator_probabilities(evolutionary_params['genetic_operator_probabilities'])

    # Make certain params globally accesable
    pysh_globals.global_max_points = evolutionary_params['max_points']

    # Prepare for multi-threading if specified by user
    if evolutionary_params["max_workers"] == None or evolutionary_params["max_workers"] > 1:
        evo_params.init_executor(evolutionary_params)

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

    # If you want to use Twilio to text you occasional updates
    if evolutionary_params['reports']['final_SMS'] or (evolutionary_params['SMS_every_x_generations'] != None and evolutionary_params['SMS_every_x_generations'] > 0):
        evo_params.setup_SMS(evolutionary_params)

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

    final_generation = 0
    stop_reason = None
    for g in range(evolutionary_params["max_generations"]):
        print()
        print("Starting Generation:", g)
        final_generation = g

        if (evolutionary_params['SMS_every_x_generations'] != None and evolutionary_params['SMS_every_x_generations'] > 0) and g > 0 and g % evolutionary_params['SMS_every_x_generations'] == 0:
            text_me.send_text_msg(evolutionary_params['run_name'] + " just reached generation " + str(g) + ".")

        start_time = datetime.datetime.now()
        if evolutionary_params['selection_method'] == 'cluster_lexicase':
            print("Clustering population by error vectors")
            all_errors = np.array([ind.get_errors() for ind in population])
            min_errors = [min(ev) for ev in all_errors.transpose()]
            # FIND ELITE ON SOMETHING!!
            evolutionary_params['clusters'] = KMeans(n_clusters=evolutionary_params["cluster_lexicase_clusters"], n_init=3).fit(all_errors)
            reporting.log_timings("clustering", start_time, datetime.datetime.now())

        # Select parents and mate them to create offspring
        print("Performing selection and variation.")
        offspring = go.genetics(population, evolutionary_params, )
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
            stop_reason = 'Solution Found'
            break # Finish evolutionary run

        if g == evolutionary_params['max_generations'] - 1:
            print('Best program in final generation:')
            print(population[0].get_program())
            print('Errors:', population[0].get_errors())
            stop_reason = 'Max Generation'

    print()
    print("Generating End of Run Reports")
    if evolutionary_params["reports"]["timings"]:
        reporting.print_timings()
    print()
    if evolutionary_params["reports"]["plot_piano_roll"]:
        reporting.plot_piano_roll()
    if evolutionary_params["reports"]["final_SMS"]:
        text_me.send_text_msg(evolutionary_params['run_name'] + " just stopped because " + str(stop_reason) + ".")



