from __future__ import absolute_import, division, print_function, unicode_literals

import random
import numpy as np

import pyshgp.utils as u
import pyshgp.push.interpreter as interp
import pyshgp.push.instruction as instr
import pyshgp.push.instructions.registered_instructions as ri
from pyshgp.push.instructions import *

##             ##
# Running Tests #
##             ##


def dict_matches_state(interpreter, state_dict):
    i = 0
    for k in state_dict.keys():
        if not state_dict[k] == interpreter.state[k]:
            return False
        i += len(state_dict[k])
    if i == len(interpreter.state):
        return True
    else:
        return False


def run_test(before, after, instruction, print_test=False):
    interpreter = interp.PushInterpreter()
    interpreter.state.from_dict(before)

    if not isinstance(instruction, instr.PyshInstruction):
        instruction = ri.get_instruction(instruction)

    if print_test:
        print(instruction.name)
        print("Before:")
        interpreter.state.pretty_print()

    if type(after) == dict:
        interpreter.execute_instruction(instruction)
        if print_test:
            print("After:")
            interpreter.state.pretty_print()
            print()
        return dict_matches_state(interpreter, after)
    else:
        try:
            interpreter.execute_instruction(instruction)
        except Exception as e:
            if print_test:
                print("Raises error: ", type(e))
                print()
            if isinstance(e, after):
                return True
            else:
                return False


##                    ##
# Generating Constants #
##                    ##

# Generating Integers


def rand_tiny_int():
    return random.randint(-10, 10)


def rand_small_int():
    return random.randint(-100, 100)


def rand_med_int():
    return random.randint(-10000, 10000)


def rand_large_int():
    return random.randint(-1000000, 1000000)


def np_int():
    return np.random.randint(-100, 100, dtype='int64')


def random_test_ints(num_of_each):
    test_ints = [0]
    for i in list(range(num_of_each)):
        test_ints += [rand_tiny_int(), rand_small_int(),
                      rand_med_int(), rand_large_int(), np_int()]
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
        test_floats += [rand_tiny_float(), rand_small_float(),
                        rand_med_float(), rand_large_float()]
    return test_floats

# Generating Chars and Strings


def random_char_str():
    a = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    b = a[:].lower()
    c = "\n\t_-+=.,;:!"
    s = a + b + c
    return random.choice(s)


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
