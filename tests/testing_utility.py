from __future__ import absolute_import, division, print_function, unicode_literals 

import random

##                    ##
# Generating Constants #
##                    ##

# Generating Integers

def rand_tiny_int():
	return random.randint(-10,10)

def rand_small_int():
	return random.randint(-100,100)

def rand_med_int():
	return random.randint(-10000,10000)

def rand_large_int():
	return random.randint(-1000000,1000000)

def random_test_ints(num_of_each):
	test_ints = [0]
	for i in list(range(num_of_each)):
		test_ints += [rand_tiny_int(), rand_small_int(), rand_med_int(), rand_large_int()]
	return test_ints

# Generating Floats

def rand_tiny_float():
	return random.rand() * 10

def rand_small_float():
	return random.rand() * 100

def rand_med_float:
	return random.rand() * 10000

def rand_large_float():
	return random.rand() * 1000000

def random_test_float(num_of_each):
	test_floats = [0.0]
	for i in list(range(num_of_each)):
		test_floats += [rand_tiny_float(), rand_small_float(), rand_med_float(), rand_large_float()]
	return test_floats

# Generating Chars and Strings

def random_char():
	return random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")

def random_st():
    s = ""
    for i in range(str_length):
        if random.random() < 0.2:
            s += " "
        else:
            s += random_char()
    return s