# _*_ coding: utf_8 _*_
"""

This problem consists of using float instructions and float constants to fit
the following polynomial:

.. literalinclude:: /../examples/tutorials/simple_regression.py
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
   :lines: 77-81

Finally, we instanciate the ``SimplePushGPEvolver``. Then we can call the
``fit`` method and pass three things: 1) The error function, 2) the number of
input values that will be supplied and 3) a list of pysh types to output.

"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np

from pyshgp.push.interpreter import PushInterpreter
from pyshgp.gp.base import REGRESSION_ATOM_GENERATORS
from pyshgp.gp.evolvers import SimplePushGPEvolver


def target_function(x):
    return x**6 + -2 * (x**4) + x**2


def error_func(program):
    errors = []
    for x in np.arange(-2.0, 2.0, 0.1):
        inpt = float(x)
        # Create the push interpreter
        interpreter = PushInterpreter([inpt], ['_float'])
        y_hat = interpreter.run(program)[0]
        # Get output
        if y_hat is None:
            errors.append(1e5)
        else:
            # compare to target output
            target_float = target_function(inpt)
            # calculate error
            errors.append((y_hat - target_float)**2)
    return errors


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1,
                              selection_method='epsilon_lexicase',
                              atom_generators=REGRESSION_ATOM_GENERATORS,
                              max_generations=50)
    evo.fit(error_func, 1, ['_float'])
