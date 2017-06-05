# _*_ coding: utf_8 _*_
"""
The goal of the Odd problem is to evolve a program that will produce a True if
the input integer is odd, and a False if its even.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random

from pyshgp.push.instructions import registered_instructions as ri
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.gp.base import SimplePushGPEvolver
from pyshgp.gp.variation import UniformMutation, Alternation
from pyshgp.utils import merge_sets

def odd_error_func(program, debug = False):
    errors = []
    for i in range(10):
        # Create the push interpreter
        interpreter = PushInterpreter([i])
        # Run program
        outputs = interpreter.run_push(program)
        # Get output
        if 'y_hat' in outputs.keys():
            y_hat = outputs['y_hat']
            #compare to target output
            y = bool(i % 2)
            if y_hat == y:
                errors.append(0)
            else:
                errors.append(1)
        else:
            errors.append(9999)
    return errors

atom_generators = list(merge_sets(ri.get_instructions_by_pysh_type("_integer"),
                                  ri.get_instructions_by_pysh_type("_boolean"),
                                  ri.get_instructions_by_pysh_type("_code"),
                                  ri.get_instructions_by_pysh_type("_exec"),
                                  [lambda: random.randint(0, 10)]))

if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=2, atom_generators=atom_generators)
    evo.fit(odd_error_func, 1, {'y_hat' : False})
