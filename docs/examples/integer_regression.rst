******************
Integer Regression
******************

.. automodule:: examples.integer_regression

Running The Example
###################

To run the integer regression problem, just run the example problem.::

    python path/to/integer_regression.py


The Error Function
##################

For a more comprehensive explainaiton of what a error function is in Pysh, see the :doc:`Odd Problem <odd>`.

Below is the error function for the Integer Regression problem.

.. literalinclude:: /../examples/integer_regression.py
   :pyobject: error_func

Integer Regression Problem Parameters
#####################################

Every evolutionary paramter has a default value that can be overwritten when defining a problem. These parameters are stored in a dictionary.

.. note::
    More infomration about the rest of the evolutionary params can be found on the :doc:`Evolutionary Parameters Page <../Evolutionary_Parameters>`.

Below is the dictionary defining the evolutionary parameters that pertain to the Integer Regression problem.

.. literalinclude:: /../examples/integer_regression.py
   :lines: 49-62

The integer regression problem only uses a small subset of Pysh's instruction set. To obtain an individual instruction we use :code:`get_instruction_by_name("instruction name")` from the registered_instructions module.

For an explaination of epigenetic markers, see :doc: `Programs Vs. Genomes`.

For an explaination of the genetic operators included in Pysh, see :doc: `Genetic Operators`.

Starting Evolution
##################

Evolution can be started by calling the `evolution` function from the `gp` module.

.. code:: python

    if __name__ == "__main__":
        gp.evolution(error_func, problem_params)

Full Source Code
################

The full source code of the Integer Regression problem file can be found on Github `here <https://github.com/erp12/Pysh/blob/master/examples/integer_regression.py>`_.