# _*_ coding: utf_8 _*_
"""
Created on 11/30/2016

@author: Eddie
"""

import pysh.utils as u
import pysh.gp.gp as gp
import pysh.push.interpreter as interp
import pysh.push.instructions.registered_instructions as ri
import pysh.push.instruction as instr


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

def invert_bitstring(bitstr):
    inverted_bitstr = []
    for b in bitstr:
        if b:
            inverted_bitstr.append(False)
        else:
            inverted_bitstr.append(True)
    return inverted_bitstr

for t in test_cases:
    print(t, invert_bitstring(t))

def error_func(program, debug = False):
    errors = []
    for t in test_cases:
        interpreter = interp.PyshInterpreter([t])
        interpreter.run_push(program, debug)
        prog_output = interpreter.state.stacks['_boolean'][:]
        target_output = invert_bitstring(t)

        if not len(prog_output) == len(target_output):
            errors.append(1000)
        else:
            errors.append(u.levenshtein_distance(prog_output, target_output))
    return errors

params = {
    "atom_generators" : list(u.merge_sets(ri.get_instructions_by_pysh_type("_boolean"),
                                          ri.get_instructions_by_pysh_type("_vector"),
                                          [instr.PyshInputInstruction(0)])),
    "max_points" : 3200,
    "max_genome_size_in_initial_program" : 400,
    "evalpush_limit" : 1600,
    "population_size" : 1000,
    "max_generations" : 300,
    "genetic_operator_probabilities" : {"alternation" : 0.2,
                                        "uniform_mutation" : 0.2,
                                        "alternation & uniform_mutation" : 0.5,
                                        "uniform_close_mutation" : 0.1},
    "alternation_rate" : 0.01,
    "alignment_deviation" : 10,
    "uniform_mutation_rate" : 0.01,
    "final_report_simplifications" : 5000

}

def test_solution():
  #print(registered_instructions.registered_instructions)
  prog_lst = [instr.PyshInputInstruction(0), '_exec_do*vector_boolean', ['_boolean_not']]
  prog = gp.load_program_from_list(prog_lst)
  errors = error_func(prog, debug = True)
  print("Errors:", errors)


if __name__ == "__main__":
    gp.evolution(error_func, params)
    #test_solution()