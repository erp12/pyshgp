
.. sidebar:: Useful Links

	* `Evolutionary Parameters <Evolutionary_Parameters.html>`_
	* `Instruction Set <Instructions.html>`_
	* `Examples <Examples.html>`_


****
Pysh
****

Push Genetic Programming in Python


Push Genetic Programming
========================

Push is programming language that plays nice with evolutionay computing / genetic programming. It is a stack-based language that features 1 stack per data type, including code. Programs are represented by lists of instructions, which modify the values on the stacks. Instuctions are executed in order.

More information about PushGP can be found `here <http://faculty.hampshire.edu/lspector/push.html>`_.

For the most cutting edge PushGP framework, see the `Clojure <https://clojure.org/>`_ implementaion called `Clojush <https://github.com/lspector/Clojush>`_.


Examples / Usage
================

* `Odd <Odd>`_
* `Integer Regression <Integer_Regression>`_


To run the Pysh examples, simply run one of the following commands from the directory into which you have placed your pysh folder.::

	python -m pysh.problems.odd
	python -m pysh.problems.simple_regression

To learn more about changing the evolutionary parameters for a genetic programming run, see the `evolutionary parameters documentation <Evolutionary_Parameters.html>`_.

For a more in depth explanation of Pysh's usage, see the examples page.


Roadmap
=======

Pysh is currently under active development. Feel free to submit a pull request if you have any additions to make.

In Progress Features
--------------------

* More complete string instructions
* Add string mutation to Uniform Mutation algorithm
* Implement utility functions to filter registered instructions by type


Future Features
---------------

* Add parallel evaluation (using SCOOP)
* Add compatibility with python 3

.. _Evolutionary Parameters: Evolutionary_Parameters.html
.. _Instruction Set: Instructions.html
.. _Examples: Examples.html


