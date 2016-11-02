****************
What is Push GP?
****************


The Push Language
=================

The following paragraph has been taken from the Push language `homepage <http://faculty.hampshire.edu/lspector/push.html>`_.

	Push is a programming language designed for evolutionary computation, to be used as the programming language within which evolving programs are expressed. Push features a stack-based execution architecture in which there is a separate stack for each data type. In Push, "code" itself is a data type, allowing programs to manipulate their own code as they run and thereby to implement arbitrary and potentially novel control structures. This expressiveness is combined with syntactic minimality: the only syntax rule is that parentheses must be balanced. It is therefore trivial to generate and transform syntactically valid Push programs.

To demonstrate how Push works, and some of its benefits, we will step through the execution of a simple Push program.

Consider the folloing program: :code:`(5 "10" string_from_integer exec_dup (string_concat integer_from_string))`

The first step to executing a push program is to push the whole program (as a list) onto the exec stack. Below is the state of the Push stacks.

========= ==============================================================================
exec:     (5 "10" string_from_integer exec_dup (string_concat integer_from_string))
integer:
string:
========= ==============================================================================

Generally, Push language implementations contain more stacks than the 3 listed above, but this example only requires the 3 thus they are the only stacks shown.

Each step of Push program execution involves 1) popping the top item off the exec stack. 2) Processing the item in the interpreter 3) Pushing the result onto the appropriate stack, when applicable.

For the first step of execution, the only item on the exec stack is a list containing the entire program. When the push interpreter encounters a list, it simply pushes the contents of the list onto the exec stack in reverse order (which preserves the execution order). The resulting state of the stacks is as follows:

========= ==============================================================================
exec:     5 "10" string_from_integer exec_dup (string_concat integer_from_string)
integer:
string:
========= ==============================================================================

At this stage in our example, the item on top of the exec stack is a 5, which is a literal value (as opposed to an instruction, which we will see later). When a literal value is processed by the interpreter, it is simply placed on the stack corresponding to its type. Thus, the new state is as follows:

========= ============================================================================
exec:     "10" string_from_integer exec_dup (string_concat integer_from_string)
integer:  5
string:
========= ============================================================================

For the next step in the program execution, the item that is now on top of the exec stack is another literal. This time it is a string. 

========= ============================================================================
exec:     string_from_integer exec_dup (string_concat integer_from_string)
integer:  5
string:   "10"
========= ============================================================================

Now the top item on the exec stack is an instruction. An instruction is a function that has access to the items on the stacks, and can push its result on to any of the stacks. Pysh contains a fairly comprehensive instruction set, documentend on the :doc:`Instruction Set Page <Instructions>`. It is also simple to define your own instructions (explained :doc:`here <custom_instructions>`).

The ``string_from_integer`` instruction is the instruction that will pop the top integer, cast it to a string, and then push the resulting string onto the string stack. Thus, the resulting state of the stacks is as follows:

========= ============================================================================
exec:     exec_dup (string_concat integer_from_string)
integer:  
string:   "5" "10"
========= ============================================================================

The next item on the exec stack is the ``exec_dup`` instruction. This instruction demonstrates the expressivness of the Push language. Push programs continue to run until the exec stack is empty. Push instructions have the ability to modify the stacks, including the exec stack. This makes it trival to create instructions that implement various forms of conditionals, modularity, and code reuse. The ``exec_dup`` instruction is one of the simplest forms of code reuse. It pushes a copy of the next item on the exec stack to the exec stack. 

========= ============================================================================
exec:     (string_concat integer_from_string) (string_concat integer_from_string)
integer:  
string:   "5" "10"
========= ============================================================================

In this case, the duplicated item was a list of instructions. We can see now that this has the potential to reuse large sections of code easily.

The top item on the exec stack is now a list. As mentioned above, the contents will be pushed onto the exec stack in reverse order.

========= ============================================================================
exec:     string_concat integer_from_string (string_concat integer_from_string)
integer:  
string:   "5" "10"
========= ============================================================================

Now the top item of the exec stack is the ``string_concat`` instruction. This instruction will concatenate the top two strings and push the result back onto the string stack.

========= ============================================================================
exec:     integer_from_string (string_concat integer_from_string)
integer:  
string:   "105"
========= ============================================================================

The ``integer_from_string`` instruction parses the top string to an integer and pushes the result to the integer stack.

========= ============================================================================
exec:     (string_concat integer_from_string)
integer:  105
string:   
========= ============================================================================

The next item on the exec stack is a list, so it will be unpacked.

========= ============================================================================
exec:     string_concat integer_from_string
integer:  105
string:   
========= ============================================================================

Next, the interpreter will encouter another ``string_concat`` instruction, but there are no items on the string stack. Push was designed so that any nested structure of literals and instructions is a valid program (assuming balanced parentheses). One important behavior of Push interpreters that helps acheive this design is how instructions are handled when the required arguments aren't present. In cases like this, the instruction is skipped over. In other words, no values are popped from the stacks except the instruction on the exec stack.

This behavior is extremely important when using the Push language in Genetic Programming frameworks (like Pysh) because randomly generated programs often contain many instructions that do not have the required instructions when executed.

The resulting state of the stack will simply be as follows:

========= ============================================================================
exec:     integer_from_string
integer:  105
string:   
========= ============================================================================

The ``integer_from_string`` instruction is also lacking arguments, and will be ignored.

========= ============================================================================
exec:     
integer:  105
string:   
========= ============================================================================

The above state is the output of the push program. The remaining items on the stacks can be utilized as needed.



Push Genetic Programming
========================

The following paragraph has been taken from the Push language `homepage <http://faculty.hampshire.edu/lspector/push.html>`_.

	PushGP is a genetic programming system that evolves programs in the Push programming language. Features include:

	- Multiple data types without constraints on code generation or manipulation.
	- Arbitrary control structures without constraints on code generation or manipulation.
	- Arbitrary modularity without constraints on code generation or manipulation.
	- Automatic program simplification.

Generating Random Programs
''''''''''''''''''''''''''

Pysh can generate random Plush genomes, rather than Push programs. The difference between Plush Genomes and Push Programs is explained in detail :doc:`here <Programs_V_Genomes>`. Plush genomes can easily be translated into Push programs and executed.

When generating random genomes, Pysh relys on **atom generators** and **epigenetic markers**.

An "atom" refers to either an instruction or a literal. **Atom generators** are things that produce an "atom". For example, an anonymous function that returns a random floating point value between 0 and 1 could be an **atom generator**. At the time of random program generation (but NOT program execution) this anonymous function could be used to generate a literal in the program. An instruction can also be considered an **atom generator** that adds itself to the random program.

When generating a random genome, Pysh selects **atom generators** at random. If the atom generator is a constant, it is added to the genome. If the atom generator is an anonymous function, it is called and its response if added to the genome. If the atom generator is an instruction, it is added to the genome. Instructions can be either registered instructions from the :doc:`Pysh instruction set <Instructions>` or one of the :doc:`special I/O instructions <Input_Output_Instr>`.

**Epigenetic Markers** are how the nested structure of a push program is captured in the linear genome. They are extra values associated with each gene that denotes if the gene places an parenthesis in the program, and/or if the gene is silent. **Epigenetic Markers** are discussed more in depth on the :doc:`Programs Vs. Genomes page <Programs_V_Genomes>`. 

When generating random individuals during PushGP, random Plush genomes are generated and translated into programs. The individuals in the evolutionary population store both their genomes and their programs. Programs are executed during the indivudals fitness evaluations, while genomes are manipulated by the genetic operators. When new genomes are needed (aka offspring) a new individual is created with the new genome, and the program for the new individual is produced by translating the new genome.


Evaluating Programs
'''''''''''''''''''

Every Genetic Programming problem requires an error function, sometimes called a fitness function. This function takes a program produced by evolution, executes it, and evaluates how well it solved the problem.

In most Push GP systems, error functions return a vector of numbers representing the program's error on each test case. The total error of the program is the sum of the error vector. During evolution, some selection methods select parents based on a program's total error, while other utilize the dis-aggregated error vector.

A program whose total error is equal to, or below, the stopping threshold paremeter (default to 0) is considered a solution.

.. note::
    Currently Pysh only supports using evolution to minimize a programs *errors*. It is also common to evaluate programs based on a *fitness* value that evolution attempts to maximize, but this is not supported by Pysh.

In Pysh, error functions are simply python functions. These



Selection and Variation
'''''''''''''''''''''''



