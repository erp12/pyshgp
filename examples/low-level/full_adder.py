# _*_ coding: utf_8 _*_
"""
Created on 11/30/2016

@author: Eddie
"""

from pyshgp.utils import merge_sets
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver
from pyshgp.gp.variation import (UniformMutation, Alternation,
                                 VariationOperatorPipeline)


cases = [(False, False, False),
         (False, False, True),
         (False, True, False),
         (False, True, True),
         (True, False, False),
         (True, False, True),
         (True, True, False),
         (True, True, True)]


def full_adder(c, a, b):
    xor_1 = not a == b
    s = not xor_1 == c

    and_1 = a and b
    and_2 = xor_1 and c
    c_out = and_1 or and_2
    return (s, c_out)


def error_function(program):
    errors = []
    for case in cases:
        interpreter = PushInterpreter(case, ['_boolean', '_boolean'])
        output = interpreter.run(program)
        targets = full_adder(case)
        e = 0

        if output[0] is None:
            e += 1000
        elif output[0] != targets[0]:
            e += 1

        if output[1] is None:
            e += 1000
        elif output[1] != targets[1]:
            e += 1

        errors.append(e)
    return errors


atom_generators = list(merge_sets(get_instructions_by_pysh_type('_boolean'),
                                  get_instructions_by_pysh_type('_exec')))
mut = UniformMutation(rate=0.1)
alt = Alternation(rate=0.1, alignment_deviation=10)
ops = [(alt, 0.2), (mut, 0.3), (VariationOperatorPipeline((mut, alt)), 0.5)]


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1, operators=ops,
                              atom_generators=atom_generators,
                              initial_max_genome_size=300,
                              population_size=500, max_generations=300,
                              simplification_steps=5000)
    evo.fit(error_function, 3, ['_boolean', '_boolean'])
