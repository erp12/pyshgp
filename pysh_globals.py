# _*_ coding: utf_8 _*_
"""
Created on Sun Jun  5 13:29:14 2016

@author: Eddie
"""
import random

from instructions import *
from instructions import registered_instructions 

pysh_types = ["_exec",
              "_integer",
              "_float",
              "_string",
              "_bool",
              "_code"]          
              
# These definitions are used by instructions to keep computed values within limits
# or when using random instructions.
max_number_magnitude = 1000000000000 # Used by keep_number_reasonable as the maximum size of any integer or float
min_number_magnitude = 1.0E-10 # Used by keep_number_reasonable as the minimum magnitude of any float
max_string_length = 5000 # Used by string instructions to ensure that strings don't get too large
max_vector_length = 5000 # Used by vector instructions to ensure that vectors don't get too large
min_random_integer = -10 # The minumum value created by the integer_rand instruction
max_random_integer = 10 # The maximum value created by the integer_rand instruction
min_random_float = -1.0 # The minumum value created by the float_rand instruction
max_random_float = 1.0 # The maximum value created by the float_rand instruction
min_random_string_length = 1 # The minimum length of string created by the string_rand instruction
max_random_string_length = 10 # The maximum length of string created by the string_rand instruction
max_points_in_random_expressions = 50 # The maximum length of code created by the code_rand instruction


global_evalpush_limit = 150 # The number of Push instructions that can be evaluated before stopping evaluation
global_evalpush_time_limit = 0 # The time in nanoseconds that a program can evaluate before stopping, 0 means no time limit




pysh_argmap = {
#
#----------------------------------------
# Epignenetics
#----------------------------------------
'epigenetic_markers' : ['_close'], # A vector of the epigenetic markers that should be used in the individuals. Implemented options include: :close, :silent
'close_parens_probabilities' : [0.772, 0.206, 0.021, 0.001], # A vector of the probabilities for the number of parens ending at that position. See random-closes in clojush.random          
'silent_instruction_probability' : 0.2, # If :silent is used as an epigenetic-marker, this is the probability of random instructions having :silent be true
#
#----------------------------------------
# Standard GP arguments
#----------------------------------------
"error_function" : lambda p: 0, # Function that takes a program and returns a list of errors
"error_threshold" : 0, # Pushgp will stop and return the best program if its total error is <= the error_threshold
"atom_generators" : registered_instructions.registered_instructions + # The instructions that pushgp will use in random code
                    [lambda: random.randint(0, 100),
                     lambda: random.random()],
"population_size" : 1000, # Number of individuals in the population
"max_generations" : 1001, # The maximum number of generations to run GP
"max_point_evaluations" : 10e100, # The limit for the number of point (instruction) evaluations to execute during the run
"max_points" : 100, # Maximum size of push programs and push code, as counted by points in the program. 1/2 this limit is used as the limit for sizes of Plush genomes.
"max_genome_size_in_initial_program" : 50, # Maximum size of initial Plush genomes in generation 0. Keep in mind that genome lengths will otherwise be limited by 1/2 of "max_points
"evalpush_limit" : 150, # The number of Push instructions that can be evaluated before stopping evaluation
"evalpush_time_limit" : 0, # The time in nanoseconds that a program can evaluate before stopping, 0 means no time limit
"reuse_errors" : True, # When true, children produced through direct reproduction will not be re_evaluated but will have the error vector of their parent
"pass_individual_to_error_function" : False # When true, entire individuals (rather than just programs) are passed to error functions


}

# print pysh_argmap['atom_generators']