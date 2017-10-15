"""
Given two vectors of integers in [-1000,1000] of the same length <= 50,
return a vector of integers that sums the other two at each index.
"""
import random

from pyshgp.utils import PushVector, merge_sets
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver


def vectors_summed(vec1: list, vec2: list) -> list:
    result_list = []
    for i in range(len(vec1)):
        result_list.append(vec1[i] + vec2[i])
    return result_list


def generate_input_vec(length: int) -> list:
    return PushVector([random.randint(-1000, 1000) for x in range(length)], int)


def generate_cases(n_cases: int) -> list:
    cases = []
    for i in range(n_cases):
        l = random.randint(1, 50)
        inpts = [generate_input_vec(l), generate_input_vec(l)]
        target = vectors_summed(*inpts)
        cases.append((inpts, target))
    return cases


training_set = generate_cases(50)
testing_set = generate_cases(50)


def error_function(program, debug=False):
    errors = []
    for case in training_set:
        interpreter = PushInterpreter(case[0], ['_vector_integer'])
        result = interpreter.run(program, debug)[0]
        if result is None:
            errors.append(1e5)
        else:
            e = []
            for i in range(min(len(result), len(case[1]))):
                e.append(abs(result[i] - case[1][i]))
            e.append(abs(len(result) - len(case[1])) * 100)
            errors.append(sum(e))
    return errors


atom_generators = list(merge_sets(
    get_instructions_by_pysh_type("_integer"),
    get_instructions_by_pysh_type("_vector_integer"),
    get_instructions_by_pysh_type("_exec"),
    [lambda: random.randint(-100, 100)]
))


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1,
                              atom_generators=atom_generators,
                              initial_max_genome_size=400)
    evo.fit(error_function, 2, ['_vector_integer'])
