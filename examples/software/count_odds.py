"""
Problem Source: iJava (http://ijava.cs.umass.edu/)

Given a vector of integers with length <= 50, with each integer in [-1000,1000],
return the number of integers that are odd.
"""
import random

from pyshgp.utils import PushVector, merge_sets
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver


def count_odds(vec: list) -> int:
    return len([x for x in vec if x % 2 == 1])


def generate_cases(n_cases: int) -> list:
    cases = []
    for i in range(n_cases):
        l = random.randint(1, 50)
        inpt = PushVector([random.randint(-1000, 1000) for x in range(l)], int)
        target = count_odds(inpt)
        cases.append((inpt, target))
    return cases


training_set = generate_cases(50)
testing_set = generate_cases(50)


def error_function(program, debug=False):
    errors = []
    for case in training_set:
        interpreter = PushInterpreter([case[0]], ['_integer'])
        result = interpreter.run(program, debug)[0]
        if result is None:
            errors.append(1e5)
        else:
            errors.append((case[1] - result) ** 2)
    return errors


atom_generators = list(merge_sets(
    get_instructions_by_pysh_type("_integer"),
    get_instructions_by_pysh_type("_boolean"),
    get_instructions_by_pysh_type("_vector_integer"),
    get_instructions_by_pysh_type("_exec"),
    [lambda: random.randint(-1000, 1000),
     lambda: PushVector([], int),
     lambda: 0, lambda: 1, lambda: 2]
))


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1,
                              atom_generators=atom_generators,
                              initial_max_genome_size=400)
    evo.fit(error_function, 1, ['_integer'])
