# _*_ coding: utf_8 _*_
"""
The goal of the Odd problem is to evolve a program that will produce a True if
the input integer is odd, and a False if its even.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

from pyshgp.push.interpreter import PushInterpreter
from pyshgp.gp.base import SimplePushGPEvolver

def odd_error_func(program, debug = False):
    errors = []

    for i in range(10):
        # Create the push interpreter
        interpreter = PushInterpreter([i])
        # Run program
        interpreter.run_push(program, debug)
        # Get output
        prog_output = interpreter.state["_boolean"].ref(0)
        #compare to target output
        target_output = bool(i % 2)

        if prog_output == target_output:
            errors.append(0)
        else:
            errors.append(1)
    return errors


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1)
    evo.evolve(odd_error_func, 1)
