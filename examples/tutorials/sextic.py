# _*_ coding: utf_8 _*_
"""
The Sextic problem is simple, floating point symbolic regression problem.

The problem consists of using float instructions and float constants to fit
the following polynomial:

.. literalinclude:: /../examples/sextic.py
    :pyobject: target_function

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np
import random

from pyshgp.push.interpreter import PushInterpreter
from pyshgp.gp.base import SimplePushGPEvolver, REGRESSION_ATOM_GENERATORS

def target_function(x):
    return x**6 + -2 * (x**4) + x**2

def error_func(program):
    errors = []
    for x in np.arange(-2.0, 2.0, 0.1):
        inpt = float(x)
        # Create the push interpreter
        interpreter = PushInterpreter([inpt])
        outputs = interpreter.run_push(program)
        # Get output
        if 'y_hat' in outputs.keys():
            y_hat = outputs['y_hat']
            # compare to target output
            target_float = target_function(inpt)
            # calculate error
            errors.append((y_hat - target_float)**2)
        else:
            errors.append(1000)

    return errors

if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1,
                              selection_method='epsilon_lexicase',
                              atom_generators=REGRESSION_ATOM_GENERATORS)
    evo.fit(error_func, 1, {'y_hat' : -9999.0})
