***
Odd
***

The goal of the Odd problem is to evolve a program that will produce a True if the input integer is odd, and a False if its even.

Running The Example
###################

To run the odd problem, install Pysh and run the example file.::

    python path/to/odd.py


The Error Function
##################

Every Genetic Programming problem requires an error function, sometimes called a fitness function. This function takes a program produced by evolution, executes it, and evaluates how well it solved the problem.

In Pysh, error functions return a vector of numbers representing the program's error on each test case. The total error of the program is the sum of the error vector. During evolution, some selection methods select parents based on a program's total error, while other utilize the dis-aggregated error vector.

A program whose total error is equal to, or below, the stopping threshold paremeter (default to 0) is considered a solution.

.. note::
    Currently Pysh only supports using evolution to minimize a programs *errors*. It is also common to evaluate programs based on a *fitness* value that evolution attempts to maximize. This feature is not yet implemented in Pysh.

Below is the error function for the odd problem.

.. code:: python

    def odd_error_func(program):
        errors = []

        for i in range(9):
            prog = copy.deepcopy(program)
            # Create the push interpreter
            interpreter = pysh_interpreter.Pysh_Interpreter()
            interpreter.reset_pysh_state()
            
            # Push input number     
            interpreter.state.stacks["_integer"].push_item(i)
            interpreter.state.stacks["_input"].push_item(i)
            # Run program
            interpreter.run_push(prog)
            # Get output
            prog_output = interpreter.state.stacks["_boolean"].stack_ref(0)
            #compare to target output
            target_output = bool(i % 2)

            if prog_output == target_output:
                errors.append(0)
            else:
                errors.append(1)
        return errors


Odd Problem Parameters
######################

Every evolutionary paramter has a default value that can be overwritten when defining a problem. These parameters are stored in a dictionary. For the odd problem most default values are used, with the exception of the *atom generators*.

.. note::
    Atom generators are instructions that pushgp will use in random code generation. More infomration about the rest of the evolutionary params can be found on the :doc:`Evolutionary Parameters Page <Evolutionary_Parameters>`.

Below is the dictionary defining the evolutionary parameters that pertain to the Odd problem.

.. code:: python

    odd_params = {
        "atom_generators" : u.merge_dicts(registered_instructions.registered_instructions,  # Use all possible instructions,
                                          {"f1" : lambda: random.randint(0, 100),           # and some integers
                                           "f2" : lambda: random.random(),                  # and some floats
                                           "Input" : instr.Pysh_Input_Instruction(0)})      # and an input instruction that pushes the input to the _integer stack.
    }

Starting Evolution
##################

Evolution can be started by calling the `evolution` function from the `gp` module.

.. code:: python

    if __name__ == "__main__":
        gp.evolution(odd_error_func, odd_params)

Full Source Code
################

The full source code of the Odd problem file can be found on Github `here <https://github.com/erp12/Pysh/blob/master/examples/odd.py>`_.