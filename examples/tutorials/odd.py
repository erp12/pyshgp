"""
The goal of the Odd problem is to evolve a program that will produce a True if
the input integer is odd, and a False if its even.

Running The Example
###################

To run the odd problem, install ``pyshgp`` and run the example file.::

    python pyshgp/examples/tutorials/odd.py

The Error Function
##################

Every Genetic Programming problem requires an error function, sometimes called
a fitness function. This function takes a program produced by evolution,
executes it, and evaluates how well it solved the problem.

In Pysh, error functions return a vector of numbers representing the program's
error on each test case. The total error of the program is the sum of the error
vector. During evolution, some selection methods select parents based on a
program's total error, while other utilize the dis-aggregated error vector.

A program whose total error is equal to, or below, the stopping threshold
paremeter (default to 0) is considered a solution.

.. literalinclude:: /../examples/tutorials/odd.py
    :pyobject: odd_error_func

.. note::
    Currently ``pyshgp`` only supports using evolution to minimize a programs
    *errors*. It is also common to evaluate programs based on a *fitness* value
    that evolution attempts to maximize. This feature is not implemented in
    ``pyshgp``.

Starting The Run
#################

Finally, we instanciate the ``SimplePushGPEvolver``. Then we can call the
``fit`` method and pass three things: 1) The error function, 2) the number of
input values that will be supplied and 3) a list of pysh types to output.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import random

from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.gp.evolvers import SimplePushGPEvolver
from pyshgp.utils import merge_sets


def odd_error_func(program, debug=False):
    errors = []
    for i in range(10):
        # Create the push interpreter
        interpreter = PushInterpreter()
        # Run program
        y_hat = interpreter.run(program, [i], ['_boolean'])[0]
        # Get output
        if y_hat is None:
            errors.append(1e5)
        else:
            # compare to target output
            y = bool(i % 2)
            if y_hat == y:
                errors.append(0)
            else:
                errors.append(1)
    return errors


atom_generators = list(merge_sets(get_instructions_by_pysh_type("_integer"),
                                  get_instructions_by_pysh_type("_boolean"),
                                  get_instructions_by_pysh_type("_code"),
                                  get_instructions_by_pysh_type("_exec"),
                                  [lambda: random.randint(0, 10)]))


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=2,
                              atom_generators=atom_generators)
    evo.fit(odd_error_func, 1, ['_boolean'])
