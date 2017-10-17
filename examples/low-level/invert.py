# _*_ coding: utf_8 _*_
"""
Created on 11/30/2016

@author: Eddie
"""
from pyshgp.utils import merge_sets, PushVector, levenshtein_distance
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
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


def invert_bitstring(bitstr):
    inverted_bitstr = []
    for b in bitstr:
        if b:
            inverted_bitstr.append(False)
        else:
            inverted_bitstr.append(True)
    return inverted_bitstr


def error_function(program, debug=False):
    errors = []
    for case in cases:
        interpreter = PushInterpreter()
        output = interpreter.run(program, [case], ['_vector_boolean'], debug)[0]
        target = invert_bitstring(case)
        if output is None:
            errors.append(1e5)
        if not len(output) == len(target):
            errors.append(1e4)
        else:
            errors.append(levenshtein_distance(output, target))
    return errors


atom_generators = list(merge_sets(get_instructions_by_pysh_type('_boolean'),
                                  get_instructions_by_pysh_type('_exec')))
mut = UniformMutation(rate=0.01)
alt = Alternation(rate=0.01, alignment_deviation=10)
ops = [(alt, 0.2), (mut, 0.3), (VariationOperatorPipeline((mut, alt)), 0.5)]


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1, operators=ops,
                              atom_generators=atom_generators,
                              initial_max_genome_size=300,
                              population_size=500, max_generations=300,
                              simplification_steps=5000)
    evo.fit(error_function, 1, ['_vector_boolean'])
