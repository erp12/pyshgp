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

To see an example push program being executed, step-by-step refer to the :doc:`What is PushGP <Push_GP>` page.


Plush Genomes
=============

Plush genomes are linear representations of Push programs. Consider the following push program:

``(5 exec_dup (10 integer_add) integer_dec)``

There are many possible plush genomes that would express this program. One genome that would translate into the above program is as follows:

+------------------+-------+----------+----------+-------+-------------+-------------+
| **Instruction:** | 5     | exec_dup | exec_rot | 10    | integer_add | integer_dec |
+------------------+-------+----------+----------+-------+-------------+-------------+
| **Closes:**      | 0     | 0        | 0        | 0     | 1           | 0           |
+------------------+-------+----------+----------+-------+-------------+-------------+
| **Silent:**      | False | False    | True     | False | False       | False       |
+------------------+-------+----------+----------+-------+-------------+-------------+

In the above table, each column represents a "gene" in the genome. 

.. note::
    In Pysh, Genes are represented as tuples. Genomes are represented as a list of gene tupels.

The **instruction** values indicate which instructions (or literals) appear in the genome. These *instruction* values also denote if the gene should place an open parentheses in the program. When defining a new instruction the number of open parentheses is specifed, and every occurence of that instruction places the specified number of open parentheses. Literal values never place open parentheses.

The **closes** count and **silent** boolean parts of each gene are considered **epigenetic markers**. These are explained below.

Epigenetic Markers
""""""""""""""""""

Epigenetic Markers are how the nested structure of a push program is captured in the linear genome. They also have the ability to "silence" a gene.

Close
'''''
As mentioned above, each instruction denotes how many open parentheses should follow it once translated into a push program. In order for a Push program to be valid, all open parentheses must be closed. One way which a close parenthesis can be added is by incrementing a genes ``close`` epigenetic marker. When a genome is translated into a program, each instruction (or literal) is followed by a number of close parentheses equal to the gene's ``close`` value, not exceeding the number of open parentheses that have not been closed. At the end of program translation a number of close parentheses are added equal to the number of un-matched open parentheses.

For example, the definition of the ``exec_dup`` instruction specifies that one open parenthesis should should follow it in the program. This is clearly seen in the example program above. In the genome, we see that the close count of the ``integer_add`` gene has been set to 1. This causes the close parenthesis that follows the ``integer_add`` instruction in the example program. 

Silent
''''''
It is also possible for genes in a plush genome to not appear in the translated program. This occurs when the **silent** epigenetic marker is true. This can be used during :doc:`Automatic Program Simplification <Simplification>` or various genetic operator.

Notice in the above genome example that the ``exec_rot`` gene has it's silent gene set to True and thus the ``exec_rot`` instruction does not appear in the program.


More Information
================
.. toctree::
   :maxdepth: 1

   Simplification
