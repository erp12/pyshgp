# _*_ coding: utf_8 _*_
"""
@author: Eddie

This example problem is meant to be a demonstration of how ``pyshgp`` could be
used to perform simple regression tasks. 

The problem consists of using integer instructions and integer constants to fit
the following polynomial: 

.. literalinclude:: /../examples/integer_regression.py
   :pyobject: target_function

The training set for this problem consists of only 20 data points.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random

import pyshgp.gp.gp as gp
import pyshgp.push.interpreter as interp
import pyshgp.push.instructions.registered_instructions as ri
import pyshgp.push.instruction as instr

def target_function(x):
    return x**3 - (2*(x**2)) - x

def error_func(program):
    errors = []

    for x in range(20):
        # Create the push interpreter and run program
        interpreter = interp.PushInterpreter(inputs=[x])
        interpreter.run_push(program)
        # Get output
        top_int = interpreter.state.stacks["_integer"].ref(0)

        if type(top_int) == int:
            # compare to target output
            target_int = target_function(x)
            # calculate error
            errors.append(abs(top_int - target_int))
        else:
            errors.append(1000)

    return errors

problem_params = {
    "atom_generators" : [ri.get_instruction('_integer_div'),
                         ri.get_instruction('_integer_mult'),
                         ri.get_instruction('_integer_add'),
                         ri.get_instruction('_integer_sub'),
                         lambda: random.randint(0, 10),
                         instr.PyshInputInstruction(0)],
    "epigenetic_markers" : [],
    "selection_method" : "epsilon_lexicase",
    "genetic_operator_probabilities" : {"alternation" : 0.5,
                                        "uniform_mutation" : 0.5},
    "alternation_rate" : 0.1,
    "uniform_mutation_rate" : 0.1
}


if __name__ == "__main__":
    gp.evolution(error_func, problem_params)

