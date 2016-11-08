*************************
Defining New Instructions
*************************

Defining your own Pysh instruction requires the following steps:

1. Writing a python function that performs the desired behavior.
2. Creating an instance of the Instruction class.
3. Adding the instruction object in the collection of registered isntructions.

1. Writing The Instruction Function
===================================

Pysh instruction functions must take a single argument: the state of the push stacks.

In Pysh, the state is a mutable object. This means that the push instructions do not have to return anything.

Before modifing the stacks, it is important for the instruction function to check if the required agruments exist on the stack. Otherwise, the function should not modify the stacks.

The followin is an example function which implements the ``string_concat`` instruction.

:: python

    def string_concat(state):
        if len(state.stacks['_string']) > 1:             # Check to make sure there are at least 2 item on the string stack, otherwise do nothing.
            s0 = state.stacks['_string'].stack_ref(0)    # Get the top item on the string stack
            s1 = state.stacks['_string'].stack_ref(1)    # Get the second item on the string stack
            state.stacks['_string'].pop_item()           # Pop top item off the string stack.
            state.stacks['_string'].pop_item()           # Pop top item again
            state.stacks['_string'].push_item(s1 + s0)   # Push the concatenated string onto the string stack.

2. Creating the Instruction Object
==================================

To create an instruction object, you need to instansiate the Instruction class found in ``instruction.py``.

Instansiating the Instruction class requires 1) The name the instruction should be registered as 2) an instruction function (described above) 3) the stack types used by the instruction and 4) the number of open parenthese that should follow the instruction, if applicable.

For our ``string_concat`` instruction, the instruction object would be created like this: 
:: python

    string_concat_instruction = instr.Pysh_Instruction('string_concat', string_concat, stack_types = ['_string'])

The second argument (``string_concat``) is a reference to the function we defined in the above section. Notice that the number of open parenthesis did not need to be specified because the default value is 0. The ``exec_do_range`` instruction should specify that one open parenthesis is inserted in the program after the instruction. The instansiation of the Instruction class would look like this:

:: python

    exec_do_range_intruction = instr.Pysh_Instruction('exec_do*range', exec_do_range, stack_types = ['_exec', '_integer'], parentheses = 1)

3. Registering Instruction
==========================



Stuff for Contributors
======================

Documenting Instructions
""""""""""""""""""""""""

Adding Instruction Unit Tests
"""""""""""""""""""""""""""""
