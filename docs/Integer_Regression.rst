
******************
Integer Regression
******************

The goal of the Integer Regression problem is to evolve a mathmatical function that will perform the same computation as a target function. This problem only deals with integers to keep the search space much smaller, compared to other symbolic regression problems.

Running The Example
###################

To run the integer regression problem, just run the example problem.::

    python path/to/integer_regression.py


The Error Function
##################

For a more comprehensive explainaiton of what a error function is in Pysh, see the :doc:`Odd Problem <Odd>`.

Below is the error function for the Integer Regression problem.

.. code:: python

    def target_function(x):
        return x**3 - (2*(x**2)) - x

    def error_func(program):
        errors = []

        for x in range(9):
            prog = copy.deepcopy(program)
            # Create the push interpreter
            interpreter = pysh_interpreter.Pysh_Interpreter()
            interpreter.reset_pysh_state()
            
            # Push input number     
            interpreter.state.stacks["_integer"].push_item(x)
            interpreter.state.stacks["_input"].push_item(x)
            # Run program
            interpreter.run_push(prog)
            # Get output
            top_int = interpreter.state.stacks["_integer"].stack_ref(0)
            #compare to target output
            target_int = target_function(x)

            if type(top_int) == int:
                errors.append(abs(top_int - target_int))
            else:
                errors.append(1000)

        return errors

Integer Regression Problem Parameters
#####################################

Every evolutionary paramter has a default value that can be overwritten when defining a problem. These parameters are stored in a dictionary.

.. note::
    More infomration about the rest of the evolutionary params can be found on the :doc:`Evolutionary Parameters Page <Evolutionary_Parameters>`.

Below is the dictionary defining the evolutionary parameters that pertain to the Integer Regression problem.

.. code:: python

    problem_params = {
        "atom_generators" : {"integer_div" : ri.get_instruction_by_name("integer_div"),
                             "integer_mult" : ri.get_instruction_by_name("integer_mult"),
                             "integer_add" : ri.get_instruction_by_name("integer_add"),
                             "integer_sub" : ri.get_instruction_by_name("integer_sub"),
                             "f1" : lambda: random.randint(0, 10),
                             "Input" : instruction.Pysh_Input_Instruction(0)},
        "epigenetic_markers" : [],
        "selection_method" : "epsilon_lexicase",
        "genetic_operator_probabilities" : {"alternation" : 0.5,
                                            "uniform_mutation" : 0.5},
        "alternation_rate" : 0.1,
        "uniform_mutation_rate" : 0.1
    }

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