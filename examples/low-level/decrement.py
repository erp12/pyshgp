# _*_ coding: utf_8 _*_
"""
Created on 11/30/2016

@author: Eddie
"""
import random
import numpy as np

from pyshgp.utils import PushVector, merge_sets
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver
from pyshgp.gp.variation import (UniformMutation, Alternation,
                                 VariationOperatorPipeline)


def gen_random_test_case():
    i = random.randint(4, 31)
    return [random.choice(list(range(i))) for _ in list(range(i))]


cases = [PushVector(gen_random_test_case(), int) for _ in range(20)]


def error_function(program):
    errors = []
    for case in cases:
        interpreter = PushInterpreter([case], ['_vector_integer'])
        output = interpreter.run(program)[0]
        target = [x - 1 for x in case]
        if output is None:
            errors.append(1e5)
        elif len(output) != len(target):
            errors.append(1e4)
        else:
            rmse = np.linalg.norm(
                np.array(output) - np.array(target)
            ) / np.sqrt(len(output))
            errors.append(rmse)
    return errors


atom_generators = list(merge_sets(get_instructions_by_pysh_type('_integer'),
                                  get_instructions_by_pysh_type('_vector'),
                                  get_instructions_by_pysh_type('_exec')))
mut = UniformMutation(rate=0.1)
alt = Alternation(rate=0.1, alignment_deviation=10)
ops = [(alt, 0.2), (mut, 0.3), (VariationOperatorPipeline((mut, alt)), 0.5)]


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1, operators=ops,
                              atom_generators=atom_generators,
                              selection_method='epsilon_lexicase',
                              initial_max_genome_size=300,
                              population_size=500, max_generations=300,
                              simplification_steps=5000)
    evo.fit(error_function, 1, ['_vector_boolean'])
