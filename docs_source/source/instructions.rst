*****************
Push Instructions
*****************

A Push instruction is object that can manipulate the typed Stacks of a ``PushState``. Typically, an instruction is defined by some function. When evaluated, the arguments to the instruction’s function are taken from the stacks of the ``PushInterpreter``’s PushState and the returned values are pushed to back to the stacks.

In PyshGP, there are a variety of classes that concretely implement the concept of an Instruction. These definitions capture all the required information about an instruction. For example, the ``SimpleInstruction`` class automatically handles the popping of arguments and pushing of returned values for functions that only require access to the top items of some stacks. Meanwhile, the more flexible ``StateToStateInstruction`` only requires a function which takes the entire PushState and returns a PushState.

Every instruction must contain information on which ``PushTypes`` it manipulates. This is so that the ``PushInterpreter`` will know which stacks to create given a collection of Instruction that will be used. It also aids in filtering collections of instructions based on what types they manipulate.

Instructions also denote how many code blocks are expected to follow the instructions. This is used during ``Genome`` to ``CodeBlock`` translation to provide the nested structure of code blocks. For example, the ``exec_if`` instruction should be followed by two code blocks: one for the "then" clause, one for the "else" clause.

With the exception of ``StateToStateInstruction`` objects, the function passed to the ``f`` argument of an Instruction must return a collection of values (either ``list`` of ``tuple``). Each element of this collection will be pushed to its respective stack after evaluation of the instruction.

If an instruction is unable to be evaluated, it can return a ``Token.revert`` object to indicate the instruction should be skipped and no change should be made to the ``PushState``. This ensures each instruction is an atomic transaction.


Example Instruction Definitions
===============================

Simple Instruction
------------------

Used when the exact function is known. In other words, how many argument are needed and their types, as well as the number of returned values and their types.

.. code-block:: python

   def protected_divison(a, b):
       if a == 0:
           return Token.revert
       return b / a,

   int_div_instr = SimpleInstruction(
       name="int_div",
       f=protected_divison,
       input_types=["int", "int"],
       output_types=["int"],
       code_blocks=0,
       docstring="Divides the top two ints and pushes the result."
   )


Produces Many Of Type Instruction
---------------------------------

Same as ``SimpleInstruction`` except that a variable number of returned values will be produced. All returned values will be of the same type.

.. code-block:: python

    def split_on_comma(s):
      return s.split(",")

    str_split_instr = ProducesManyOfTypeInstruction(
        "str_split_on_comma",
        split_on_comma,
        input_types=["str"],
        output_type="str",
        code_blocks=0,
        docstring="Pushes multiple strs produced by splitting the top str on all commas.".format(t=push_type)
    )

Takes State Instruction
-----------------------

Same as ``SimpleInstruction`` except that the argument to the function is the entire ``PushState``. This is typically used when a variable number of elements are needed as input or one of the ``PushState``'s other attributes are needed to determine the result.

.. code-block:: python

    def bool_stack_depth(state):
      return len(state["bool"]),

    bool_depth_instr = TakesStateInstruction(
        "bool_stack_depth",
        bool_stack_depth,
        output_types=["int"],
        other_types=["bool"],
        code_blocks=0,
        docstring="Pushes the size of the bool stack to the int stack."
    )

State-to-State Instruction
--------------------------

An Instruction that takes entire ``PushState`` and returns entire ``PushState``.

.. code-block:: python

    def exec_when(state):
        if state["exec"].is_empty() or state["bool"].is_empty():
            return Token.revert
        if not state["bool"].pop():
            state["exec"].pop()
        return state

    exec_when_instr = StateToStateInstruction(
        "exec_when",
        exec_when,
        types_used=["exec"],
        code_blocks=1,
        docstring="""Pops the next item on the exec stack without evaluating it
        if the top bool is False. Otherwise, has no effect."""
    )

Preparing Instruction Sets
==========================

To specify which instructions should be used during program synthesis (Specifically during gene spawning, and genome variation), PyshGP utilizes an InstructionSet object. Instructions can be added, or “registered,” into an InsturctionSet as long as the instructions name is unique across the set.

PyshGp contains a collection of “core” instructions that work with the typical data types. Subsets of the “core” instruction can easily be registered using the methods of the InstructionSet object.

.. code-block:: python

    instruction_set = (
        InstructionSet()
        .register_by_type(
          ["int", "bool", "stdout"], # All core instructions that manipulate any of these types...
          exclude=["str"]            # ... but remove any instructions that any of these types.
        )
        .register_by_name(".*_add")  # All core instructions with name matching regex.
        .register_n_inputs(2)        # Register 2 input instructions when arity 2 programs are synthesized.
    )

If custom instructions are instantiated (either via a provided class or by extending the Instruction abstract base class) they can also be registered in an InstructionSet.

Defining Instructions which manipulate custom PushTypes or custom PushStacks is not currently supported, however it will be future versions.

Registering Custom Instructions
-------------------------------

.. code-block:: python

    instruction_set.register(int_div_instr)
    instruction_set.register_list([str_split_instr, bool_depth_instr, exec_when_instr])
