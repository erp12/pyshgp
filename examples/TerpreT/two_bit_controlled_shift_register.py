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


test_cases = [(0, 0, 0),
              (0, 0, 1),
              (0, 1, 0),
              (0, 1, 1),
              (1, 0, 0),
              (1, 0, 1),
              (1, 1, 0),
              (1, 1, 1)]

def error_func(program):
    errors = []
    for t in test_cases:
        interpreter = interp.PyshInterpreter(t)
        interpreter.run_push(program)
        prog_output = interpreter.state.stacks['_integer'][-2:]

        e = 0
        if len(prog_output) < 2:
            e += 1000
        else:
            if t[0] == 1:
                if not prog_output[0] == t[2]:
                    e += 1
                if not prog_output[1] == t[1]:
                    e += 1
            else:
                if not prog_output[0] == t[1]:
                    e += 1
                if not prog_output[1] == t[2]:
                    e += 1
        errors.append(e)
    return errors

params = {
    "atom_generators" : list(u.merge_sets(ri.registered_instructions,
                                          [instr.PyshInputInstruction(0),
                                           instr.PyshInputInstruction(1),
                                           instr.PyshInputInstruction(2)])),
    "genetic_operator_probabilities" : {"alternation" : 0.2,
                                        "uniform_mutation" : 0.2,
                                        "alternation & uniform_mutation" : 0.5,
                                        "uniform_close_mutation" : 0.1},
    "alternation_rate" : 0.01,
    "alignment_deviation" : 10,
    "uniform_mutation_rate" : 0.01,
    "final_report_simplifications" : 5000
}

if __name__ == "__main__":
    gp.evolution(error_func, params)