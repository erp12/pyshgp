"""
Given a vector of integers of length <= 50, each integer in the range [-50,50],
at least one of which is 0, return the index of the last occurance of 0 in the
vector.
"""
import random

from pyshgp.utils import PushVector, merge_sets
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver


def last_index_of_zero(vec: list) -> int:
    return len(vec) - 1 - vec[::-1].index(0)


def generate_input_vector() -> PushVector:
    l = random.randint(1, 50)
    input_lst = []
    for i in range(l):
        if random.random() < 0.1:
            input_lst.append(0)
        else:
            input_lst.append(random.randint(-50, 50))
    # By the problem definition, there must be at least 1 zero.
    zero_ndx = random.randint(0, l - 1)
    input_lst[zero_ndx] = 0
    return PushVector(input_lst, int)


def generate_cases(n_cases: int) -> list:
    cases = []
    for i in range(n_cases):
        inpt = generate_input_vector()
        target = last_index_of_zero(inpt)
        cases.append((inpt, target))
    return cases


training_set = generate_cases(200)
testing_set = generate_cases(100)


def error_function(program, debug=False):
    errors = []
    for case in training_set:
        interpreter = PushInterpreter()
        result = interpreter.run(program, [case[0]], ['_integer'], debug)[0]
        if result is None:
            errors.append(1e6)
        else:
            errors.append(abs(result - case[1]))
    return errors


atom_generators = list(merge_sets(
    get_instructions_by_pysh_type("_integer"),
    get_instructions_by_pysh_type("_boolean"),
    get_instructions_by_pysh_type("_vector_integer"),
    get_instructions_by_pysh_type("_exec"),
    [lambda: random.randint(-50, 50)]
))

if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1,
                              atom_generators=atom_generators,
                              initial_max_genome_size=150,
                              max_generations=300)
    evo.fit(error_function, 1, ['_integer'])
