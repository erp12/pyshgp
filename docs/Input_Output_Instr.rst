*****************************
Input and Output Instructions
*****************************

Input Instructions
==================

Pysh uses the same input instruction system that most modern PushGP systems use. The system utilizes a designated input stack that is pre-loaded with the inputs to the program before execution. Various instruction found in Push programs can copy items from within the input stack and place them on their designated type stack during the execution of the program.

Input instructions are explained in more detail on `this page of the Push Redux <https://erp12.github.io/push-redux/pages/input_instr/index.html>`_.

Printing Instructions
=====================

After a push program is executed, all values remaining on the stacks of the push state are considered returned outputs of the program. Occasionally, Push programs must also print values during execution. In most standard languages this would be handled by printing to :code:`stdout`, which is not able to be captured by fitness functions during evolution. To remedy this, Pysh borrows a technique found in most modern PushGP implementations.

A designated :code:`output` stack is used which contains a single empty string before program execution. As the program is executed, if one of the various :code:`print` instructions may be called. These instruction take values off the stacks in the Push state and append them to the string on the bottom element of the :code:`output` stack. After program execution the string that has been built up over the course of program execution is considered the printed output of the program.

Printing instructions are explained in more detail on `this page of the Push Redux <https://erp12.github.io/push-redux/pages/output_instr/index.html>`_.


Class Voting Instructions
=========================

Class Voting instructions are used when PushGP is applied to classification problems. If one of these instructions is called during the execution of a push program, an element from either the :code:`integer` or :code:`float` stack is taken and added to the votes for a particular class. These votes are stored on index 1 through C of the :code:`output` stack, where C is the number of classes and index 0 is the printing string mentioned in the section above.

Class Voting instructions are explained in more detail on `this page of the Push Redux <https://erp12.github.io/push-redux/pages/output_instr/index.html>`_.
