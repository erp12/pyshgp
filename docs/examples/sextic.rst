****************************
Sextic (Symbolic Regression)
****************************

.. automodule:: examples.sextic

Running The Example
###################

To run the odd problem, install Pysh and run the example file.::

    python path/to/sextic.py


The Error Function
##################

.. literalinclude:: /../examples/sextic.py
   :pyobject: error_func

.. note::
    For a more comprehensive explainaiton of what am error function is in Pysh, 
    see the :doc:`Odd Problem <odd>`.


Sextic Parameters
#################

Below is the sextic problem specific parameters. 

.. literalinclude:: /../examples/sextic.py
   :lines: 47-66

The most notable parameter for the sextic progrem is that it uses 
``epsilon_lexicase`` as its selection method. This selection method is discussed
in greater detail on the `Genetic Operators <Genetic_Operators>`_ page.

For regression problems, it is helpful to have a small, non-zero 
``error_threshold`` because perfect solutions are difficult to evolve.

The sextic ``atom_generators`` consist of basic floating point math 
instructions, random floating point constants, and a single input instruction.

There is no need for ``epigenetic_markers``, because nested structures are not
required to solve this problem.

Starting Evolution
##################

Evolution can be started by calling the `evolution` function from the `gp`
module.

.. code:: python

    if __name__ == "__main__":
        gp.evolution(error_func, problem_params)

Full Source Code
################

The full source code of the Odd problem file can be found on Github 
`here <https://github.com/erp12/Pysh/blob/master/examples/sextic.py>`_.