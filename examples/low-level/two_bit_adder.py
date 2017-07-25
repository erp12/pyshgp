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

cases = [(False, False, False, False),
         (False, False, False, True),
         (False, False, True, False),
         (False, False, True, True),
         (False, True, False, False),
         (False, True, False, True),
         (False, True, True, False),
         (False, True, True, True),
         (True, False, False, False),
         (True, False, False, True),
         (True, False, True, False),
         (True, False, True, True),
         (True, True, False, False),
         (True, True, False, True),
         (True, True, True, False),
         (True, True, True, True)]


def one_bit_adder(c, a, b):
    xor_1 = not a == b
    s = not xor_1 == c

    and_1 = b and c
    and_2 = a and c
    and_3 = a and b
    c_out = and_1 or and_2 or and_3
    return (s, c_out)


def two_bit_adder(a_1, b_1, a_2, b_2):
    tmp_1 = one_bit_adder(0, a_1, b_1)
    s_1 = tmp_1[0]

    tmp_2 = one_bit_adder(tmp_1[1], a_2, b_2)
    s_2 = tmp_2[0]
    c_out = not tmp_1[1] == tmp_2[1]
    return (s_1, s_2, c_out)


def error_function(program):
    errors = []
    for case in cases:
        interpreter = PushInterpreter(case,
                                      ['_boolean', '_boolean', '_boolean'])
        outputs = interpreter.run(program)
        target = two_bit_adder(case[0], case[1], case[2], case[3])
        e = 0

        if outputs[0] is None:
            e += 1e4
        elif outputs[0] == target[0]:
            e += 1

        if outputs[1] is None:
            e += 1e4
        elif outputs[1] == target[1]:
            e += 1

        if outputs[2] is None:
            e += 1e4
        elif outputs[2] == target[2]:
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
