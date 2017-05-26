# _*_ coding: utf_8 _*_
"""
The Replace Space With Newline problem is an insteresting software synthesis
problem. The RSWN problem is specified as:

Given a string input, print the string, replacing spaces with newlines.
The input string will not have tabs or newlines, but may have multiple spaces
in a row. It will have maximum length of 20 characters. Also, the program
should return the integer count of the non-whitespace characters.

This problem requires PushGP to evolve a program that manipulates more than
one data type. This problem aslo requires the printing of a value on top of
producing another value.
"""


from __future__ import absolute_import, division, print_function, unicode_literals

import random

from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instructions import registered_instructions as ri
from pyshgp.push.instruction import PyshInputInstruction
from pyshgp.gp.base import SimplePushGPEvolver
from pyshgp.gp.variation import UniformMutation, Alternation
from pyshgp.utils import (UnevaluatableStackResponse, Character, merge_sets,
                          test_and_train_data_from_domains,
                          levenshtein_distance)


def random_str(str_length):
    s = ""
    for i in range(str_length):
        if random.random() < 0.2:
            s += " "
        else:
            s += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    return s


def make_RSWN_data_domains():
    dd_1 = {"inputs": ["", "A", "*", " ", "s", "B ", "  ", " D", "ef", "!!", " F ", "T L", "4ps", "q  ", "   ", "  e", "hi ", "  $  ", "      9",
                       "i !i !i !i !i", "88888888888888888888", "                    ", "ssssssssssssssssssss", "1 1 1 1 1 1 1 1 1 1 ",
                       " v v v v v v v v v v", "Ha Ha Ha Ha Ha Ha Ha", "x y!x y!x y!x y!x y!", "G5G5G5G5G5G5G5G5G5G5", ">_=]>_=]>_=]>_=]>_=]",
                       "^_^ ^_^ ^_^ ^_^ ^_^ "],
            "train_test_split": [30, 0]}
    dd_2 = {"inputs": lambda: random_str(random.randint(2, 19)),
            "train_test_split": [0, 0]}  # 70 , 1000
    return (dd_1, dd_2)


def RSWN_test_cases(inputs):
    '''
    Takes a sequence of inputs and gives IO test cases of the form [input output].
    [inpt_str [target_str, taget_int]]
    '''
    return list(map(lambda inpt: [inpt, [str.replace(str(inpt), " ", "\n"), len(list(filter(lambda x: not x == " ", inpt)))]], inputs))


def make_RSWN_error_func_from_cases(train_cases):
    def actual_RSWN_func(program, debug=False):
        errors = []

        for io_pair in train_cases:
            interpreter = PushInterpreter([io_pair[0]])
            interpreter.run_push(program, debug)
            str_result = interpreter.state["_string"].ref(0)
            int_result = interpreter.state["_integer"].ref(0)

            if isinstance(str_result, UnevaluatableStackResponse):
                # If response is un-evaluatable, add a bad error.
                errors += [1000, 1000]
            else:
                # If response is evaluatable, compute actual error
                s_er = levenshtein_distance(io_pair[1][0], str_result)
                i_er = 1000
                if type(int_result) == int:
                    i_er = abs(int_result - io_pair[1][1])
                errors += [s_er, i_er]

        return errors
    return actual_RSWN_func


def get_RSWN_train_and_test():
    '''
    Returns the train and test cases.
    '''
    data_domains = make_RSWN_data_domains()
    io_pairs = list(
        map(RSWN_test_cases, test_and_train_data_from_domains(data_domains)))
    return io_pairs


atom_generators = list(merge_sets(
    ri.get_instructions_by_pysh_type("_integer"),
    ri.get_instructions_by_pysh_type("_boolean"),
    ri.get_instructions_by_pysh_type("_string"),
    ri.get_instructions_by_pysh_type("_char"),
    ri.get_instructions_by_pysh_type("_exec"),
    ri.get_instructions_by_pysh_type("_print"),
    [  # Constants
        lambda: Character(" "),
        lambda: Character("\n"),
        # ERCs
        lambda: Character(random.choice(
            "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\n\t")),
        lambda: random_str(
            random.randint(0, 21)),
        # Input instruction
        PyshInputInstruction(0)]))

if __name__ == "__main__":
    train_and_test = get_RSWN_train_and_test()
    err_func = make_RSWN_error_func_from_cases(train_and_test[0])
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1,
                              atom_generators=atom_generators,
                              initial_max_genome_size=400,
                              )
    evo.evolve(err_func, 1)
