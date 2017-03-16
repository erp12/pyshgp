# _*_ coding: utf_8 _*_
"""
This problem evolves a program to determine if a number is odd or not.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random

import pyshgp.utils as u
import pyshgp.gp.gp as gp
import pyshgp.push.interpreter as interp
import pyshgp.push.instructions.registered_instructions as ri
import pyshgp.push.instruction as instr

def odd_error_func(program, debug = False):
    errors = []

    for i in range(10):
        # Create the push interpreter
        interpreter = interp.PushInterpreter([i])
        # Run program           
        interpreter.run_push(program, debug)
        # Get output
        prog_output = interpreter.state.stacks["_boolean"].ref(0)
        #compare to target output
        target_output = bool(i % 2)

        if prog_output == target_output:
            errors.append(0)
        else:
            errors.append(1)
    return errors

odd_params = {
    "atom_generators" : list(u.merge_sets(ri.registered_instructions,
                                          [lambda: random.randint(0, 100),
                                           lambda: random.random(),
                                           instr.PyshInputInstruction(0)]))
}

def test_odd_solution():
    #print(registered_instructions.registered_instructions)
    prog_lst = [2, '_integer_mod', 1, '_integer_eq']
    prog = gp.load_program_from_list(prog_lst)
    errors = odd_error_func(prog, debug = True)
    print("Errors:", errors)


if __name__ == "__main__":
    gp.evolution(odd_error_func, odd_params)
    #test_odd_solution()

