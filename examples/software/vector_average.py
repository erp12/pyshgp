"""
Given a vector of floats with length in [1,50], with each float in
[-1000,1000], return the average of those floats. Results are rounded to 4
decimal places.
"""
import random

from pyshgp.utils import PushVector, merge_sets
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver


def generate_cases(n_cases: int) -> list:
    cases = []
    for i in range(n_cases):
        l = random.randint(1, 50)
        inpt = PushVector([random.randint(-1000, 1000) for x in range(l)], int)
        target = sum(inpt) / len(inpt)
        cases.append((inpt, target))
    return cases


training_set = generate_cases(50)
testing_set = generate_cases(50)


def error_function(program, debug=False):
    errors = []
    for case in training_set:
        interpreter = PushInterpreter()
        result = interpreter.run(program, [case[0]], ['_float'], debug)[0]
        if result is None:
            errors.append(1e5)
        else:
            errors.append((result - case[1]) ** 2)
    return errors


atom_generators = list(merge_sets(
    get_instructions_by_pysh_type("_integer"),
    get_instructions_by_pysh_type("_float"),
    get_instructions_by_pysh_type("_vector_float"),
    get_instructions_by_pysh_type("_exec"),
    [lambda: PushVector([], float)]
))


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1,
                              atom_generators=atom_generators,
                              initial_max_genome_size=400)
    evo.fit(error_function, 1, ['_float'])
