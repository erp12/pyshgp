*************************
Defining New Instructions
*************************

Defining your own Pysh instruction requires the following steps:

1. Writing a python function that performs the desired behavior.
2. Creating an instance of the Instruction class.
3. Adding the instruction object in the collection of registered instructions.

1. Writing The Instruction Function
===================================

Pysh instruction functions must take a single argument: the state of the push stacks.

In Pysh, the state is a mutable object. This means that the push instructions do not have to return anything.

Before modifying the stacks, it is important for the instruction function to check if the required arguments exist on the stack. Otherwise, the function should not modify the stacks.

The following is an example function which implements the ``string_concat`` instruction.

.. code:: python

    def string_concat(state):
        if len(state.stacks['_string']) > 1:             # Check to make sure there are at least 2 item on the string stack, otherwise do nothing.
            s0 = state.stacks['_string'].stack_ref(0)    # Get the top item on the string stack
            s1 = state.stacks['_string'].stack_ref(1)    # Get the second item on the string stack
            state.stacks['_string'].pop_item()           # Pop top item off the string stack.
            state.stacks['_string'].pop_item()           # Pop top item again
            state.stacks['_string'].push_item(s1 + s0)   # Push the concatenated string onto the string stack.

2. Creating the Instruction Object
==================================

To create an instruction object, you need to instantiate the Instruction class found in ``instruction.py``.

Instantiating the Instruction class requires 1) The name the instruction should be registered as 2) an instruction function (described above) 3) the stack types used by the instruction and 4) the number of open parentheses that should follow the instruction, if applicable.

For our ``string_concat`` instruction, the instruction object would be created like this: 

.. code:: python

    string_concat_instruction = instr.Pysh_Instruction('string_concat', string_concat, stack_types = ['_string'])

The second argument (``string_concat``) is a reference to the function we defined in the above section. Notice that the number of open parenthesis did not need to be specified because the default value is 0. The ``exec_do_range`` instruction should specify that one open parenthesis is inserted in the program after the instruction. The instantiation of the Instruction class would look like this:

.. code:: python

    exec_do_range_intruction = instr.Pysh_Instruction('exec_do*range', exec_do_range, stack_types = ['_exec', '_integer'], parentheses = 1)

3. Registering Instruction
==========================

Once you have created the instruction object, if will need to be added to the collection of registered instructions. To do this, simply pass the instruction object to the ``register_instruction()`` function found in ``instructions/registered_instructions.py``.

If doing this raises a warning, it is likely that there is already an instruction registered with the name you chosen. Change the name field of your instruction object and try again. 


Stuff for Contributors
======================

Documenting Instructions
""""""""""""""""""""""""

Pysh currently has quick-and-dirty approach to documenting the instruction set. Following the definition of each instruction in every module in the `instructions/` folder, there is some comment lines that contain documentation on the instruction. Consider the following definition of the ``string_concat`` instruction.

.. code:: python

    def string_concat(state):
        if len(state.stacks['_string']) > 1:
            s0 = state.stacks['_string'].stack_ref(0)
            s1 = state.stacks['_string'].stack_ref(1)
            state.stacks['_string'].pop_item()
            state.stacks['_string'].pop_item()
            state.stacks['_string'].push_item(s1 + s0)
    string_concat_instruction = instr.Pysh_Instruction('string_concat',
                                                       string_concat,
                                                       stack_types = ['_string'])
    registered_instructions.register_instruction(string_concat_instruction)
    #<instr_open>
    #<instr_name>string_concat
    #<instr_desc>Pops top 2 strings, and pushes result of concatenating those strings to the string stack.
    #<instr_close>

As more instructions are added to the Pysh instruction set, these comments are parsed and used to create the :doc:`Instructions <Instructions>` page. If you intend on contributing instructions to Pysh, it would be very helpful if you include these instruction documentation comments as well.

Adding Instruction Unit Tests
"""""""""""""""""""""""""""""

Pysh contains a set of "instruction unit tests" which are used to test the instruction set. These test are run using Python 2.7 and Python 3.5.

Each test executes a small push program that demonstrates the behavior of a particular instruction, and compares the resulting state of the stacks against what should be expected after executing the instruction.

Examples of these tests can be found in the Pysh Github Repository in the `Pysh/tests/test_instruction_set.py <https://github.com/erp12/Pysh/blob/master/tests/test_instruction_set.py>`_ file. If you intend on contributing instructions to Pysh, it would be very helpful if you include at least one instruction unit test. 


