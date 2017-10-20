"""
Given 4 integers, print the smallest of them.
"""
import random

from pyshgp.utils import merge_sets
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver
from pyshgp.gp.variation import (
    PerturbCloseMutation,
    UniformMutation,
    Alternation,
    VariationOperatorPipeline)


def generate_cases(n_cases: int) -> list:
    cases = []
    for i in range(n_cases):
        inpts = [random.randint(-100, 100) for x in range(4)]
        target = str(min(inpts))
        cases.append((inpts, target))
    return cases


training_set = generate_cases(50)
training_set = generate_cases(50)


def error_function(program, debug=False):
    errors = []
    for case in training_set:
        interpreter = PushInterpreter()
        interpreter.run(program, case[0], [], debug)
        result = interpreter.state.stdout
        if result is None:
            errors.append(1e5)
        else:
            errors.append(int(result != case[1]))
    return errors


atom_generators = list(merge_sets(
    get_instructions_by_pysh_type("_integer"),
    get_instructions_by_pysh_type("_boolean"),
    get_instructions_by_pysh_type("_print"),
    get_instructions_by_pysh_type("_exec"),
    [lambda: random.randint(-100, 100)]
))


alternation = Alternation(rate=0.01, alignment_deviation=5)
mutation = UniformMutation(rate=0.01)
genetic_operators = [
    (alternation, 0.2),
    (mutation, 0.2),
    (PerturbCloseMutation(rate=0.1), 0.1),
    (VariationOperatorPipeline((alternation, mutation)), 0.5)
]


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=2,
                              atom_generators=atom_generators,
                              initial_max_genome_size=400,
                              operators=genetic_operators,
                              population_size=1000,
                              max_generations=200)
    evo.fit(error_function, 4, [])
