# _*_ coding: utf_8 _*_
"""
Created on Sun Jun  5 13:29:14 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random

pysh_types = ["_exec",
              "_integer",
              "_float",
              "_string",
              "_char",
              "_boolean",
              "_code",
              "_input",
              "_output"]          
              
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
global_max_points = 200 # Maximum size of push programs and push code, as counted by points in the program. Also, the maximum size of code that can appear on the exec or code stacks.
