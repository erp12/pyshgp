********************
Programs Vs. Genomes
********************

Info coming soon!

Push Programs
=============

Push programs are lists and nested lists of *instructions* and *literals* that are intended to be run through a Push interpreter. The push interpreter contains a stack for each data type. The state of these stacks is modified by the Push program when it is executed with the interpreter. 

Literals
""""""""

Literals are constants (or primitive) values. Examples of literals include: the integer ``3``, the string ``"HelloWorld"``, the boolean ``TRUE``, and the floating point number ``3.14``. When literals are processed by the push interpreter, they are simply placed onto the stack corrisponding to their data type. (ie. The string ``"HelloWorld"`` will be pushed onto the string stack.) 

Instructions
""""""""""""

Instructions are functions that modify the state of the stacks. They are passed the state of the stacks as the only argument. When called by the push interpreter, instructions can pop items off the stacks, perform some computation, and push the resulting values back onto the stacks. For example, the ``integer_add`` instruction received the state of the stacks when it is called. It then pops the top two items off the integer stack, sums them, and pushes the resulting integer back onto the integer stack.

Pysh (and most Push language implementations) contain a set of instructions that attempt to cover most basic computations that should appear in programs. To read more about Pysh's built in instruction set, see :doc:`this page <Instructions>`. It is also possible to add more instructions to Pysh's instruction set. More information about creating new instructions can be found on the :doc:`Custom Instructions <custom_instructions>` page. 

To see an example push program being executed, step-by-step refer to the :doc:`What is PushGP? <Push_GP>` page.


Plush Genomes
=============

Plush genomes are linear representations of Push programs. 

Epigenetic Markers
""""""""""""""""""

Epigenetic Markers are how the nested structure of a push program is captured in the linear genome. They also have the ability to "silence" a gene.

Each plush gene denotes how many open parenthesis should follow it once translated into a push program. This value comes from type of instruction.



More Information
================
.. toctree::
   :maxdepth: 1

   Simplification
