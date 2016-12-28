# _*_ coding: utf_8 _*_
"""
Created on 12/1/2016

@author: Eddie
"""

import pyshgp.utils as u
import pyshgp.gp.gp as gp
import pyshgp.push.interpreter as interp
import pyshgp.push.instructions.registered_instructions as ri
import pyshgp.push.instruction as instr


test_cases = [u.PushVector([False, False, False, False], bool),
              u.PushVector([False, False, False, True], bool),
              u.PushVector([False, False, True, False], bool),
              u.PushVector([False, False, True, True], bool),
              u.PushVector([False, True, False, False], bool),
              u.PushVector([False, True, False, True], bool),
              u.PushVector([False, True, True, False], bool),
              u.PushVector([False, True, True, True], bool),
              u.PushVector([True, False, False, False], bool),
              u.PushVector([True, False, False, True], bool),
              u.PushVector([True, False, True, False], bool),
              u.PushVector([True, False, True, True], bool),
              u.PushVector([True, True, False, False], bool),
              u.PushVector([True, True, False, True], bool),
              u.PushVector([True, True, True, False], bool),
              u.PushVector([True, True, True, True], bool),
              u.PushVector([False, False, False, False, True, False, True, True], bool),
              u.PushVector([False, False, False, True, True, True, False, True], bool),
              u.PushVector([False, False, True, False, True, True, True, False], bool),
              u.PushVector([False, False, True, True, True, True, False, True], bool),
              u.PushVector([False, True, False, False, True, False, True, True], bool),
              u.PushVector([False, True, True, False, True, True, True, True], bool),
              u.PushVector([False, False, False, False, False, False, False, False], bool),
              u.PushVector([False, True, True, True, False, True, False, True], bool)]

def binary_decrement(bitstr):
    bits = list(bitstr[::-1])
    for i, bit in enumerate(bits):
        if bit:
            bits[i] = False
            break
        else:
            bits[i] = True
    return bits[::-1]

for t in test_cases:
    print(t, binary_decrement(t))
print()

def error_func(program):
    errors = []
    for t in test_cases:
        interpreter = interp.PyshInterpreter([t])
        interpreter.run_push(program)
        prog_output = interpreter.state.stacks['_boolean'][:]
        target_output = binary_decrement(t)

        if isinstance(prog_output, u.UnevaluatableStackResponse):
            errors.append(1000)
        else:
            errors.append(u.levenshtein_distance(prog_output, target_output))
    return errors

params = {
    "atom_generators" : list(u.merge_sets(ri.registered_instructions,
                                          [instr.PyshInputInstruction(0)])),
    "genetic_operator_probabilities" : {"alternation" : 0.2,
                                        "uniform_mutation" : 0.2,
                                        "alternation & uniform_mutation" : 0.5,
                                        "uniform_close_mutation" : 0.1},
    "max_points" : 3200,
    "max_genome_size_in_initial_program" : 400,
    "evalpush_limit" : 1600,
    "population_size" : 1000,
    "max_generations" : 300,
    "alternation_rate" : 0.01,
    "alignment_deviation" : 10,
    "uniform_mutation_rate" : 0.01,
    "final_report_simplifications" : 5000

}

if __name__ == "__main__":
    gp.evolution(error_func, params)