Pysh
====

Push Genetic Programming in Python. For the most complete documentation,
refer to the `ReadTheDocs`_.

Push Genetic Programming
------------------------

Push is programming language that plays nice with evolutionay computing
/ genetic programming. It is a stack-based language that features 1
stack per data type, including code. Programs are represented by lists
of instructions, which modify the values on the stacks. Instuctions are
executed in order.

More information about PushGP can be found here:
http://faculty.hampshire.edu/lspector/push.html

For the most cutting edge PushGP framework, see the `Clojure`_
implementaion called `Clojush`_.

Installing Pysh
---------------

    Pysh is compatale with python ``2.7.x`` and ``3.5.x``

Install from Pip
~~~~~~~~~~~~~~~~

Coming soon!

Build Frome source
~~~~~~~~~~~~~~~~~~

1. Clone the repo
2. ``cd`` into the pysh repo directory
3. run ``python setup.py install``
4. Thats it! Check out the examples and `Pysh ReadTheDocs`_ for in depth
   usage.

Example Usage
~~~~~~~~~~~~~

To run one of the examples, such as the odd problem, simply run
``python [/path/to/pysh]/examples/odd.py``

Odd problem source:

.. code:: python

    from __future__ import absolute_import, division, print_function, unicode_literals

    import random

    import pyshgp.utils as u
    import pyshgp.gp.gp as gp
    import pyshgp.push.interpreter as interp
    import pyshgp.push.instructions.registered_instructions as ri
    import pyshgp.push.instruction as instr


    '''
    This problem evolves a program to determine if a number is odd or not.
    '''

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

    if __name__ == "__main__":
        gp.evolution(odd_error_func, odd_params)

More demonstrations of this can be found on `Pysh’s ReadTheDocs page`_.

Pysh Roadmap / Contributing
---------------------------

Pysh is continuously being developed for applications of genetic
proramming, as well as reasearch in Evolutionary Computation.

You can see what is coming up next for Pysh on its `Roadmap`_.

Feel free to submit pull requests and I will review them when I get a
cha

.. _ReadTheDocs: http://pysh2.readthedocs.io/en/latest/index.html
.. _Clojure: https://clojure.org/
.. _Clojush: https://github.com/lspector/Clojush
.. _Pysh ReadTheDocs: http://pysh2.readthedocs.io/en/latest/index.html
.. _Pysh’s ReadTheDocs page: http://pysh2.readthedocs.io/en/latest/index.html
.. _Roadmap: https://github.com/erp12/Pysh/projects/1