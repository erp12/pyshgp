# _*_ coding: utf_8 _*_
"""
The :mod:`constants` module provides global variables that are used by
the push interpreter and GP modules.

These definitions are mostly used by instructions to keep computed values within
limitscor when using random instructions. These values do not generally need
to be tuned to improve GP performance.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

#: List of stack types that the ``pyshgp`` Push interpreter can handle.
pysh_types = ["_exec", "_integer", "_float", "_string", "_char", "_boolean", "_code",
              "_input", "_output", '_auxiliary',
              "_vector_integer", '_vector_float', '_vector_boolean', '_vector_string']    

#: Used by keep_number_reasonable as the maximum size of any integer or float
max_number_magnitude = 1000000000000 

#: Used by keep_number_reasonable as the minimum magnitude of any float
min_number_magnitude = 1.0E-10 

#: Used by string instructions to ensure that strings don't get too large
max_string_length = 5000 

#: Used by vector instructions to ensure that vectors don't get too large
max_vector_length = 5000 

#: The minumum value created by the integer_rand instruction
min_random_integer = -10 

#: The maximum value created by the integer_rand instruction
max_random_integer = 10 

#: The minumum value created by the float_rand instruction
min_random_float = -1.0 

#: The maximum value created by the float_rand instruction
max_random_float = 1.0 

#: The minimum length of string created by the string_rand instruction
min_random_string_length = 1 

#: The maximum length of string created by the string_rand instruction
max_random_string_length = 10 

#: The maximum length of code created by the code_rand instruction
max_points_in_random_expressions = 50 


#: The number of Push instructions that can be evaluated before stopping evaluation
global_evalpush_limit = 150 

#: The time in nanoseconds that a program can evaluate before stopping, 0 means no time limit
global_evalpush_time_limit = 0 

#: Maximum size of push programs and push code, as counted by points in the 
#: program. Also, the maximum size of code that can appear on the exec or 
#: code stacks. This is set during evolution, but also has a default value here
#: for push executions that happen outside of evolution.
global_max_points = 200
