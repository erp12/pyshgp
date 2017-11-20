"""
Given a vector of integers in [-1000,1000] with length <= 50, return the vector
where alll netative integers have been replaced by 0.
"""
import random

from pyshgp.utils import PushVector, levenshtein_distance, merge_sets
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver


def negative_to_zero(vec: list) -> list:
    return [0 if x < 0 else x for x in vec]


def generate_cases(n_cases: int) -> list:
    cases = []
    for i in range(n_cases):
        l = random.randint(1, 50)
        inpt = PushVector([random.randint(-1000, 1000) for x in range(l)], int)
        target = negative_to_zero(inpt)
        cases.append((inpt, target))
    return cases


training_set = generate_cases(50)
testing_set = generate_cases(50)


def error_function(program, debug=False):
    errors = []
    for case in training_set:
        interpreter = PushInterpreter()
        result = interpreter.run(program, [case[0]], ['_vector_integer'], debug)[0]
        if result is None:
            errors.append(1e5)
        else:
            errors.append(levenshtein_distance(case[1], result))
    return errors


atom_generators = list(merge_sets(
    get_instructions_by_pysh_type("_integer"),
    get_instructions_by_pysh_type("_boolean"),
    get_instructions_by_pysh_type("_vector_integer"),
    get_instructions_by_pysh_type("_exec"),
    [lambda: 0,
     lambda: PushVector([], int)]
))


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1,
                              atom_generators=atom_generators,
                              initial_max_genome_size=400,
                              selection_method='lexicase')
    evo.fit(error_function, 1, ['_vector_integer'])
