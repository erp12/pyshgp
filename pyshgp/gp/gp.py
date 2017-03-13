# _*_ coding: utf_8 _*_

"""
The :mod:`gp` module defines the genetic programming capabilities of pyshgp.
The functions in this module are responsible for creating populations,
evaluating individuals, and defining the core evolutionary loop that will be 
used to drive evolution.

.. todo::
    Create more general abstraction of evolution, probably in the form of a 
    class. Include extentions for scikit-learn.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import datetime

from .. import utils as u
from .. import exceptions as e
from .. import constants as c
from ..push import random as r
from ..push import simplification as simp
from ..push import instruction as instr

from ..push.instructions import registered_instructions as ri
from ..push.instructions import *

from . import individual
from . import operators as go
from . import monitors as monitor
from . import reporting
from . import params

def normalize_genetic_operator_probabilities(gen_op_dict):
    """Normalizes dict of operator probabilities so that values sum to 1.

    :param dict gen_op_dict: Dict where keys are operator names and values are probabilities. 
    :returns: ``gen_op_dict`` where values sum to 1 and relative magnitude preserved.
    """
    tot = sum(gen_op_dict.values())
    new_probs = [round(x / tot, 4) for x in gen_op_dict.values()]
    return dict(zip(gen_op_dict.keys(), new_probs))


def load_program_from_list(lst):
    """Loads a program from a list, and checks each string in list for an instruction with the same name.

    .. warning::
        This function will attempt to look up all strings in the registered
        instructions to see if an instruction with a matching name exists. 
        This limits you to only using strings that are not exact matches of
        instruction names. This is mitigated by the fact that all instruction
        names begin with a ``'_'``.

    :param list lst: List that should be translated into a Push program.
    :returns: List that can be executed as a Push program.
    """
    program = []
    for el in lst:
        # For each element in the list
        if type(el) == int or type(el) == float or type(el) == bool or type(el) == u.Character or type(el) == u.PushVector:
            # If ``el`` is an int, float, bool, Character object or PushVector object simply 
            # append to the program because these are push literals.
            program.append(el)
        elif type(el) == instr.PyshInstruction or type(el) == instr.PyshInputInstruction or type(el) == instr.PyshClassVoteInstruction:
            # If ``el`` an instance of any of the instruction types, append to the program.
            program.append(el)
        elif (sys.version_info[0] == 3 and (type(el) is str or type(el) is bytes)) or (sys.version_info[0] == 2 and (type(el) is str or type(el) is unicode)):
            # If ``el`` is a string:
            el = str(el)
            # Attempt to find an instruction with ``el`` as its name.
            matching_instruction = None
            try:
                matching_instruction = ri.get_instruction(el)
            except e.UnknownInstructionName():
                pass
            # If matching_instruction is None, it must be a ssring literal.
            if matching_instruction == None:
                program.append(el)
            else:
                program.append(matching_instruction)
        elif type(el) == list:
            # If ``el`` is a list (but not PushVector) turn it into a program
            # and append it to (aka. nest it in) the program.
            program.append(load_program_from_list(el))
    return program

def generate_random_population(evolutionary_params):
    """Generate random population based on given evolutionary_params.

    :param dict evolutionary_params: Dict of evolutionary hyper-parameters.
    :returns: A list of Individual objects with randomly generated genomes and translated programs.
    """
    population = []
    for i in range(evolutionary_params["population_size"]):
        rand_genome = r.random_plush_genome(evolutionary_params)
        new_ind = individual.Individual(rand_genome, evolutionary_params)
        population.append(new_ind)
    return population

def evaluate_individual(ind, error_function):
    """Adds an error vector to an individual evaluated on the given error_function.

    :param Individual ind: An instance of the Individual class.
    :param function error_function: Python function that evaluates an individual based on its program.
    :return: Individual with error values assigned.
    """
    if ind.get_errors() == []: # Only evaluate the individual if it hasn't been already.
        errors = error_function(ind.get_program())
        reporting.total_errors_in_evalutaion_order.append(sum(errors))
        ind.set_errors(errors)
    return ind


def evaluate_population(population, error_function, evolutionary_params):
    """Updates the errors of the population.

    :param list population: List of Individual objects
    :param function error_function: Python function that evaluates an individual based on its program.
    :param dict evolutionary_params: Other parameters (see params.py)
    :returns: New population (list of Individuals) with error values assigned.
    """
    if evolutionary_params['parallel_evaluation'] and (evolutionary_params["max_workers"] == None or evolutionary_params["max_workers"] > 1):
        # If parallel evalutation, map over the pool.
        pool = evolutionary_params['pool']
        return pool.map(evaluate_individual, population, [error_function]*len(population))
    else:
        # If serial evaluation
        return [evaluate_individual(ind, error_function) for ind in population]

def evolution(error_function, problem_params):
    """Basic evolutionary loop. Currently the main GP function in ``pyshgp``.

    .. todo::
        This should soon be replaced by various base classes. These classes will
        include: 1) Evolver - A general evolution class with same functionality 
        as this function 2) SymbolicRegressor - A class that extends 
        scikit-learn for regression problems and 3) SymbolicClassifier - A class
        that extends scikit-learn for classification problems.

    :param function error_function: Python function that evaluates an individual based on its program.
    :param dict problem_params: Evolutionary params that should overide the pyshgp defaults for this run.
    """ 

    # Get the params for the run
    evolutionary_params = u.merge_dicts(params.default_evolutionary_params, problem_params)
    params.grab_command_line_params(evolutionary_params)
    evolutionary_params['genetic_operator_probabilities'] = normalize_genetic_operator_probabilities(evolutionary_params['genetic_operator_probabilities'])

    # Make certain params globally accesable
    c.global_max_points = evolutionary_params['max_points']

    # Prepare for multi-threading if specified by user
    if evolutionary_params["max_workers"] == None or evolutionary_params["max_workers"] > 1:
        params.init_executor(evolutionary_params)

    # Print the params for the run
    print()
    print("=== Starting GP Run With Following Parameters ===")
    params.params_pretty_print(evolutionary_params)
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

    stop_reason = None
    for g in range(evolutionary_params["max_generations"]):
        print()
        print("Starting Generation:", g)

        start_time = datetime.datetime.now()
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
        #population = sorted(population, key=lambda ind: ind.get_total_error())
        
        # Print things user wants to monitor
        monitor.print_monitors(population, evolutionary_params["things_to_monitor"])

        # Check for any solutions
        solutions = [ind for ind in population if ind.get_total_error() <= evolutionary_params["error_threshold"]]
        if len(solutions) > 0:
            print()
            print("Solution Found On Generation " + str(g) + ":")
            print("Program:")
            print(solutions[0].get_program())
            print("Genome:")
            print(solutions[0].get_genome())
            print()
            simp.auto_simplify(solutions[0], error_function, evolutionary_params["final_simplification_steps"])
            stop_reason = 'Solution Found'
            break # Finish evolutionary run

        if g == evolutionary_params['max_generations'] - 1:
            print()
            print('Failure')
            print('Best program in final generation:')
            print(population[0].get_program())
            print('Errors:', population[0].get_errors())
            stop_reason = 'Max Generation'

    print()
    print("Generating End of Run Reports")
    if evolutionary_params["reports"]["timings"]:
        reporting.print_timings()
    print()



