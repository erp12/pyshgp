# _*_ coding: utf_8 _*_
"""
Created on 12/1/2016

@author: Eddie
"""

from pyshgp.utils import PushVector, levenshtein_distance
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.gp.evolvers import SimplePushGPEvolver
from pyshgp.gp.variation import (UniformMutation, Alternation,
                                 VariationOperatorPipeline)


cases = [PushVector([False, False, False, False], bool),
         PushVector([False, False, False, True], bool),
         PushVector([False, False, True, False], bool),
         PushVector([False, False, True, True], bool),
         PushVector([False, True, False, False], bool),
         PushVector([False, True, False, True], bool),
         PushVector([False, True, True, False], bool),
         PushVector([False, True, True, True], bool),
         PushVector([True, False, False, False], bool),
         PushVector([True, False, False, True], bool),
         PushVector([True, False, True, False], bool),
         PushVector([True, False, True, True], bool),
         PushVector([True, True, False, False], bool),
         PushVector([True, True, False, True], bool),
         PushVector([True, True, True, False], bool),
         PushVector([True, True, True, True], bool),
         PushVector([False, False, False, False, True, False, True, True],
                    bool),
         PushVector([False, False, False, True, True, True, False, True],
                    bool),
         PushVector([False, False, True, False, True, True, True, False],
                    bool),
         PushVector([False, False, True, True, True, True, False, True],
                    bool),
         PushVector([False, True, False, False, True, False, True, True],
                    bool),
         PushVector([False, True, True, False, True, True, True, True],
                    bool),
         PushVector([False, False, False, False, False, False, False, False],
                    bool),
         PushVector([False, True, True, True, False, True, False, True],
                    bool)]


def binary_decrement(bitstr):
    bits = list(bitstr[::-1])
    for i, bit in enumerate(bits):
        if bit:
            bits[i] = False
            break
        else:
            bits[i] = True
    return bits[::-1]


def error_function(program):
    errors = []
    for case in cases:
        interpreter = PushInterpreter([case], ['_vector_boolean'])
        output = interpreter.run(program)[0]
        if output is None:
            errors.append(1e5)
        else:
            target = binary_decrement(case)
            errors.append(levenshtein_distance(output, target))
    return errors


mut = UniformMutation(rate=0.01)
alt = Alternation(rate=0.01, alignment_deviation=10)
ops = [(alt, 0.2), (mut, 0.3), (VariationOperatorPipeline((mut, alt)), 0.5)]


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1, operators=ops,
                              initial_max_genome_size=300,
                              population_size=500, max_generations=300,
                              simplification_steps=5000)
    evo.fit(error_function, 1, ['_vector_boolean'])
