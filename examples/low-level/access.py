# _*_ coding: utf_8 _*_
"""
Created on 11/30/2016

@author: Eddie
"""

import random

import pyshgp.utils as u
import pyshgp.gp.gp as gp
import pyshgp.push.interpreter as interp
import pyshgp.push.instructions.registered_instructions as ri
import pyshgp.push.instruction as instr

def gen_random_test_case():
    i = random.randint(4, 31)
    j = random.randint(0, i-1)
    return [u.PushVector([random.choice(list(range(i)))for _ in list(range(i))], int), j]

test_cases = [[u.PushVector([1, 1, 2, 3, 5, 8, 13], int), 4],
              [u.PushVector([13, 11, 7, 5, 3, 2], int), 2],
             ] + [gen_random_test_case() for _ in list(range(20))]

def error_func(program):
    errors = []
    for t in test_cases:
        interpreter = interp.PushInterpreter(t)
        interpreter.run_push(program)
        prog_output = interpreter.state.stacks['_integer'].ref(0)
        target_output = t[0][t[1]]

        if isinstance(prog_output, u.UnevaluatableStackResponse):
            errors.append(1000)
        elif prog_output == target_output:
            errors.append(0)
        else:
            errors.append(1)
    return errors

params = {
    "atom_generators" : list(u.merge_sets(ri.get_instructions_by_pysh_type("_integer"),
                                          [instr.PyshInputInstruction(0),
                                           instr.PyshInputInstruction(1)])),
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
  prog_lst = [instr.PyshInputInstruction(1), instr.PyshInputInstruction(0), vector_integer_nth]
  prog = gp.load_program_from_list(prog_lst)
  errors = error_func(prog, debug = True)
  print("Errors:", errors)

if __name__ == "__main__":
    gp.evolution(error_func, params)
