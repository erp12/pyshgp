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

import random

from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instructions.numbers import (
    I_add_integer, I_sub_integer, I_mult_integer, I_div_integer)
from pyshgp.gp.evolvers import SimplePushGPEvolver


def target_function(x):
    return (x ** 3) - (2 * x ** 2) - x


def error_func(program):
    errors = []
    for x in range(10):
        # Create the push interpreter
        interpreter = PushInterpreter()
        y_hat = interpreter.run(program, [x], ['_integer'])[0]
        # Get output
        if y_hat is None:
            errors.append(1e5)
        else:
            # compare to target output
            y_target = target_function(x)
            # calculate error
            errors.append(abs(y_hat - y_target))
    return errors


atom_generators = [
    lambda: random.randint(0, 10),
    I_add_integer,
    I_sub_integer,
    I_mult_integer,
    I_div_integer
]


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=2,
                              selection_method='epsilon_lexicase',
                              atom_generators=atom_generators,
                              max_generations=50,
                              keep_linear=True)
    evo.fit(error_func, 1, ['_integer'])
