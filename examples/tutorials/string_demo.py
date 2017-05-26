# _*_ coding: utf_8 _*_
"""
Created on 7/25/2016

@author: Eddie
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import random
import collections

from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instructions import registered_instructions as ri
from pyshgp.push.instruction import PyshInputInstruction
from pyshgp.gp.base import SimplePushGPEvolver
from pyshgp.gp.variation import UniformMutation, Alternation
from pyshgp.utils import NoStackItem, StackOutOfBounds

'''
Take the input string, remove the last 2 characters, and then concat this result with itself.
The fitness will be the number of non-matching characters in the resulting string. For example,
desired result of "abcde" would be "abcabc", and a string of "abcabcrrr" would have an error of 3, for
3 too many characters, and the string "aaaaaa" would have error of 4, since it gets 2 of the characters right.
'''


def string_difference(s1, s2):
    """Returns the difference in the strings, based on character position.
    """
    char_lvl_diff = 0
    for c1, c2 in zip(s1, s2):
        char_lvl_diff += int(not c1 == c2)
    return char_lvl_diff + abs(len(s1) - len(s2))


def string_char_counts_difference(s1, s2):
    """
    """
    result = len(s1) + len(s2)
    s1_letters = collections.Counter(s1)
    for c in s2:
        if c in s1_letters:
            result -= 2
            s1_letters[c] -= 1
            if s1_letters[c] == 0:
                s1_letters.pop(c, None)
    return result


def random_str():
    s = ""
    for i in range(random.randint(1, 10)):
        s += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    return s


def string_error_func(program):
    inputs = ["abcde", "", "E", "Hi", "Tom", "leprechaun", "zoomzoomzoom",
              "qwertyuiopasd", "GallopTrotCanter", "Quinona", "_abc"]
    errors = []

    for inpt in inputs:
        # Create the push interpreter
        interpreter = PushInterpreter([inpt])
        interpreter.run_push(program)
        # Get output
        prog_output = interpreter.state["_string"].ref(0)

        if isinstance(prog_output, NoStackItem) or isinstance(prog_output, StackOutOfBounds):
            # If response is un-evaluatable, add a bad error.
            errors.append(1000)
        else:
            # compare to target output
            target_output = inpt[:-2] + inpt[:-2]
            errors.append(string_difference(prog_output, target_output) +
                          string_char_counts_difference(prog_output, target_output))
    return errors

ops = [
    (UniformMutation(constant_tweak_rate=0.8), 0.5),
    (Alternation(), 0.5)
]

atom_generators = [PyshInputInstruction(0),
                   ri.get_instruction("_string_length"),
                   ri.get_instruction("_string_head"),
                   ri.get_instruction("_string_concat"),
                   ri.get_instruction("_string_stack_depth"),
                   ri.get_instruction("_string_swap"),
                   ri.get_instruction("_string_dup"),
                   ri.get_instruction("_integer_add"),
                   ri.get_instruction("_integer_sub"),
                   ri.get_instruction("_integer_dup"),
                   ri.get_instruction("_integer_swap"),
                   ri.get_instruction("_integer_stack_depth"),
                   lambda: random.randint(0, 10),
                   lambda: random_str()]

if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1, operators=ops,
                              atom_generators=atom_generators)
    evo.evolve(string_error_func, 1)
