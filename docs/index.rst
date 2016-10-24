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


Table Of Contents
=================

.. toctree::
   :maxdepth: 1

   Evolutionary_Parameters
   Instructions
   Examples
   Push_GP
   Genetic_Operators
   Programs_V_Genomes


Installation
============

Install from Pip
""""""""""""""""

Coming soon!

Build Frome source
""""""""""""""""""

1. Clone the repo
2. :code:`cd` into the pysh repo directory
3. run :code:`python setup.py install`

Thats it! You should be ready to use Pysh.

Examples / Usage
================

Pysh is compatable with Python 2.7 and Python 3.5.

* `Odd <Odd>`_
* `Integer Regression <Integer_Regression>`_


To run the Pysh examples, simply run one of the following commands from the directory into which you have placed your pysh folder.::

	python -m pysh.problems.odd
	python -m pysh.problems.simple_regression

To learn more about changing the evolutionary parameters for a genetic programming run, see the `evolutionary parameters documentation <Evolutionary_Parameters.html>`_.

For a more in depth explanation of Pysh's usage, see the `examples page <Examples.html>`_.


Roadmap
=======

Pysh is currently under active development. Feel free to submit a pull request if you have any additions to make.

To see what features are in development, or planned for the future, check out the Github project board `here <https://github.com/erp12/Pysh/projects/1>`_.

To see Pysh's release notes, check out the other Github project board `here <https://github.com/erp12/Pysh/projects/2>`_.