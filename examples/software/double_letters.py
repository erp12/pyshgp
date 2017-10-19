"""
Problem Source: iJava (http://ijava.cs.umass.edu/)

Given a string, print the string, doubling every letter character, and
trippling every exclamation point. All other non-alphabetic and non-exclamation
characters should be printed a single time each. The input string will have
maximum length of 20 characters.
"""
import random
import string

from pyshgp.utils import levenshtein_distance, merge_sets, Character
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver


def double_letters_target(s: str) -> str:
    s = [c + c if c.isalpha() else c for c in s]
    s = ['!!!' if c == '!' else c for c in s]
    return s


def generate_cases(n_cases: int) -> list:
    cases = []
    for i in range(n_cases):
        l = random.randint(1, 20)
        inpt = [random.choice(string.printable) for i in range(l)]
        target = double_letters_target(inpt[:])
        cases.append((inpt, target))
    return cases


training_set = generate_cases(200)
testing_set = generate_cases(100)


def error_function(program, debug=False):
    errors = []
    for case in training_set:
        interpreter = PushInterpreter()
        interpreter.run(program, [case[0]], [], debug)
        result = interpreter.state.stdout
        if result is None:
            errors.append(1e5)
        else:
            errors.append(levenshtein_distance(case[1], result))
    return errors


atom_generators = list(merge_sets(
    get_instructions_by_pysh_type("_integer"),
    get_instructions_by_pysh_type("_boolean"),
    get_instructions_by_pysh_type("_string"),
    get_instructions_by_pysh_type("_char"),
    get_instructions_by_pysh_type("_exec"),
    get_instructions_by_pysh_type("_print"),
    [lambda: Character('!')]
))

if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1,
                              atom_generators=atom_generators,
                              initial_max_genome_size=400,
                              max_generations=300)
    evo.fit(error_function, 1, [])
