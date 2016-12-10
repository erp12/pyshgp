# _*_ coding: utf_8 _*_
"""
Created on 11/30/2016

@author: Eddie
"""

import random
import collections

from pysh import pysh_interpreter
from pysh import instruction as instr
from pysh import utils as u
from pysh import pysh_globals as g
from pysh.gp import gp
from pysh.instructions import boolean, code, common, numbers, string, vectors
from pysh.instructions import registered_instructions as ri


test_cases = [g.PushVector([False, False, False, False], bool),
              g.PushVector([False, False, False, True], bool),
              g.PushVector([False, False, True, False], bool),
              g.PushVector([False, False, True, True], bool),
              g.PushVector([False, True, False, False], bool),
              g.PushVector([False, True, False, True], bool),
              g.PushVector([False, True, True, False], bool),
              g.PushVector([False, True, True, True], bool),
              g.PushVector([True, False, False, False], bool),
              g.PushVector([True, False, False, True], bool),
              g.PushVector([True, False, True, False], bool),
              g.PushVector([True, False, True, True], bool),
              g.PushVector([True, True, False, False], bool),
              g.PushVector([True, True, False, True], bool),
              g.PushVector([True, True, True, False], bool),
              g.PushVector([True, True, True, True], bool),
              g.PushVector([False, False, False, False, True, False, True, True], bool),
              g.PushVector([False, False, False, True, True, True, False, True], bool),
              g.PushVector([False, False, True, False, True, True, True, False], bool),
              g.PushVector([False, False, True, True, True, True, False, True], bool),
              g.PushVector([False, True, False, False, True, False, True, True], bool),
              g.PushVector([False, True, True, False, True, True, True, True], bool),
              g.PushVector([False, False, False, False, False, False, False, False], bool),
              g.PushVector([False, True, True, True, False, True, False, True], bool)]

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
        interpreter = pysh_interpreter.Pysh_Interpreter()
        
        interpreter.state.stacks["_input"].push_item(t)
        interpreter.run_push(program, debug)
        prog_output = interpreter.state.stacks['_boolean'][:]
        target_output = invert_bitstring(t)

        if prog_output == '_no_stack_item' or prog_output == '_stack_out_of_bounds_item':
            errors.append(1000)
        else:
            errors.append(u.levenshtein_distance(prog_output, target_output))
    return errors

params = {
    "atom_generators" : u.merge_dicts(ri.get_instructions_by_pysh_type("_boolean"),
                                      ri.get_instructions_by_pysh_type("_vector"),
                                      {"Input0" : instr.Pysh_Input_Instruction(0)}),
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
  prog_lst = [instr.Pysh_Input_Instruction(0), '_exec_do*vector_boolean', ['_boolean_not']]
  prog = gp.load_program_from_list(prog_lst)
  errors = error_func(prog, debug = True)
  print("Errors:", errors)


if __name__ == "__main__":
    gp.evolution(error_func, params)
    #test_solution()