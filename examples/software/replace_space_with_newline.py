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
import random

from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver
from pyshgp.utils import Character, merge_sets, levenshtein_distance


def rswn(s: str) -> (str, int):
    new_s = s.replace(' ', '\n')
    i = len(''.join(new_s.split()))
    return (new_s, i)


required_training_cases = [(s, rswn(s)) for s in [
    "", "A", "*", " ", "s", "B ", "  ", " D", "ef", "!!", " F ", "T L", "4ps",
    "q  ", "   ", "  e", "hi ", "  $  ", "      9", "i !i !i !i !i",
    "88888888888888888888", "                    ", "ssssssssssssssssssss",
    "1 1 1 1 1 1 1 1 1 1 ", " v v v v v v v v v v", "Ha Ha Ha Ha Ha Ha Ha",
    "x y!x y!x y!x y!x y!", "G5G5G5G5G5G5G5G5G5G5", ">_=]>_=]>_=]>_=]>_=]",
    "^_^ ^_^ ^_^ ^_^ ^_^ "
    ]]


def random_str(str_length):
    s = ""
    for i in range(str_length):
        if random.random() < 0.2:
            s += " "
        else:
            s += random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
    return s


def generate_cases(n_cases: int) -> list:
    cases = []
    for i in range(n_cases):
        l = random.randint(1, 20)
        inpt = random_str(l)
        targets = rswn(inpt)
        cases.append((inpt, targets))
    return cases


training_set = required_training_cases + generate_cases(50)
testing_set = generate_cases(50)


def error_function(program, debug=False):
    errors = []
    for io_pair in training_set:
        interpreter = PushInterpreter([io_pair[0]], ['_integer'])
        int_result = interpreter.run(program, debug)[0]
        str_result = interpreter.state.stdout

        int_error = None
        str_error = levenshtein_distance(io_pair[1][0], str_result)
        if int_result is None:
            # If response is un-evaluatable, add a bad error.
            int_error = 1e5
        else:
            int_error = abs(int_result - io_pair[1][1])
        errors += [str_error, int_error]
    return errors


atom_generators = list(merge_sets(
    get_instructions_by_pysh_type("_integer"),
    get_instructions_by_pysh_type("_boolean"),
    get_instructions_by_pysh_type("_string"),
    get_instructions_by_pysh_type("_char"),
    get_instructions_by_pysh_type("_exec"),
    get_instructions_by_pysh_type("_print"),
    [lambda: Character(" "),
     lambda: Character("\n"),
     # ERCs
     lambda: Character(random.choice(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789\n\t")),
     lambda: random_str(random.randint(0, 21))]))

if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1,
                              atom_generators=atom_generators,
                              initial_max_genome_size=400)
    evo.fit(error_function, 1, ['_integer'])
