****************************
Sextic (Symbolic Regression)
****************************

The sextic problem is a symbolic regression problem. 

Running The Example
###################

To run the odd problem, install Pysh and run the example file.::

    python path/to/sextic.py


The Error Function
##################

.. code:: python

def error_func(program):
    errors = []

    for x in np.arange(-2.0, 2.0, 0.1):
        x = float(x)
        # Create the push interpreter
        interpreter = pysh_interpreter.Pysh_Interpreter()
        interpreter.reset_pysh_state()
        
        # Push input number     
        interpreter.state.stacks["_float"].push_item(x)
        interpreter.state.stacks["_input"].push_item(x)
        # Run program
        interpreter.run_push(program)
        # Get output
        top_float = interpreter.state.stacks["_float"].stack_ref(0)

        if type(top_float) == float:
            # compare to target output
            target_float = target_function(x)
            # calculate error
            errors.append((top_float - target_float)**2)
        else:
            errors.append(1000)

    return errors

.. note::
    For a more comprehensive explainaiton of what a error function is in Pysh, see the :doc:`Odd Problem <Odd>`.


Sextic Parameters
#################

Below is the sextic problem specific parameters. 

.. code:: python

    problem_params = {
        "error_threshold" : 0.01,
        "population_size" : 2000,
        "atom_generators" : {"float_div"    : ri.get_instruction_by_name("float_div"),
                             "float_mult"   : ri.get_instruction_by_name("float_mult"),
                             "float_sub"    : ri.get_instruction_by_name("float_sub"),
                             "float_add"    : ri.get_instruction_by_name("float_add"),
                             "float_rot"    : ri.get_instruction_by_name("float_rot"),
                             "float_swap"   : ri.get_instruction_by_name("float_swap"),
                             "float_dup"    : ri.get_instruction_by_name("float_dup"),
                             "float_pop"    : ri.get_instruction_by_name("float_pop"),
                             "f1"           : lambda: float(random.randint(0, 21) - 10),
                             "Input"      : instruction.Pysh_Input_Instruction(0)},
        "epigenetic_markers" : [],
        "selection_method" : "epsilon_lexicase",
        "genetic_operator_probabilities" : {"alternation" : 0.5,
                                            "uniform_mutation" : 0.5},
        "uniform_mutation_constant_tweak_rate" : 0.1,
        "uniform_mutation_float_gaussian_standard_deviation" : 0.1
    }

The most notable parameter for the sextic progrem is that it uses ``epsilon_lexicase`` as its selection method. This selection method is discussed in greater detail on the `Genetic Operators <Genetic_Operators>`_ page.

For regression problems, it is helpful to have a small, non-zero ``error_threshold`` because perfect solutions are difficult to evolve.

The sextic ``atom_generators`` consist of basic floating point math instructions, random floating point constants, and a single input instruction.

There is no need for ``epigenetic_markers``, because nested structures are not required to solve this problem.

Starting Evolution
##################

Evolution can be started by calling the `evolution` function from the `gp` module.

.. code:: python

    if __name__ == "__main__":
        gp.evolution(error_func, problem_params)

Full Source Code
################

The full source code of the Odd problem file can be found on Github `here <https://github.com/erp12/Pysh/blob/master/examples/sextic.py>`_.