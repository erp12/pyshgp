# _*_ coding: utf_8 _*_
"""

This problem consists of using float instructions and float constants to fit
the following polynomial:

.. literalinclude:: /../examples/tutorials/sextic.py
    :pyobject: target_function

Running The Example
###################

To run this problem, install ``pyshgp`` and run the example file.::

    python pyshgp/examples/tutorials/simple_regression.py

The Error Function
##################

Simply takes the difference between each prediction and the target value to
produce the error vector.

.. literalinclude:: /../examples/tutorials/simple_regression.py
   :pyobject: error_func


Starting The Run
#################

This problem contains real valued errors, and thus it is recomended to use
``epsilon_lexicase`` as the selection method.

Also the ``REGRESSION_ATOM_GENERATORS`` are used because only numeric
operations

.. literalinclude:: /../examples/tutorials/simple_regression.py
   :lines: 75-80

Finally, we instanciate the ``SimplePushGPEvolver``. Then we can call the
``fit`` method and pass three things: 1) The error function, 2) the number of
input values that will be supplied and 3) the intial state of the
`output structure <>`_.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

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
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=2,
                              selection_method='epsilon_lexicase',
                              atom_generators=REGRESSION_ATOM_GENERATORS,
                              max_generations=50)
    evo.fit(error_func, 1, {'y_hat' : -1.0e4})
