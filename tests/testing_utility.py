from __future__ import absolute_import, division, print_function, unicode_literals 

import random

import pysh.utils as u

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
	return random.random() * 10

def rand_small_float():
	return random.random() * 100

def rand_med_float():
	return random.random() * 10000

def rand_large_float():
	return random.random() * 1000000

def random_test_floats(num_of_each):
	test_floats = [0.0]
	for i in list(range(num_of_each)):
		test_floats += [rand_tiny_float(), rand_small_float(), rand_med_float(), rand_large_float()]
	return test_floats

# Generating Chars and Strings

def random_char_str():
	return random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 _-+=.,;:!\n\t")

def random_character():
	return u.Character(random_char_str())

def random_test_characters(num):
	test_chars = []
	for i in list(range(num)):
		test_chars.append(random_character())
	return test_chars

def random_str():
    s = ""
    for i in range(abs(rand_small_int())):
        s += random_char_str()
    return s

def random_test_strings(num):
	test_strs = [""]
	for i in list(range(num)):
		test_strs.append(random_str())
	return test_strs

# Generating Bools

def random_test_bools():
	return [True, False]



