*****************
Genetic Operators
*****************

.. toctree::
   :maxdepth: 1

.. note::
    To learn more about Selection, Mutation, and Recombination algorithms, I woud highly recomend the "Field Guide To Genetic Programming" book, which is freely shared online `here <http://dces.essex.ac.uk/staff/rpoli/gp-field-guide/A_Field_Guide_to_Genetic_Programming.pdf>`_. WARNING: The exact algorithms discussed in that book will not be identical to those in Pysh, because the field guide mostly discusses standard tree GP, not PushGP.

Selection
=========

A selection event refers to the points during evolution where an individual is e probabilistically chosen based on fitness. Individuals with better fitness (ie. lower error) are more likely to be chosen. The chosen individuals are typically used as "parents" in Mutaion or Recombination.

Lexicase Selection
""""""""""""""""""

Lexicase selection is the default selection method for Pysh.

    "Unlike most traditional parent selection techniques, lexicase selection does not base selection on a fitness value that is aggregated over all test cases; rather, it considers test cases one at a time in random order" 
    -- T. Helmuth, L. Spector

Lexicase selection follows the following procedure:

1. Set **candidates** to be the entire population.
2. Set **cases** to be a list of all of the test cases in random order.
3. Loop:
    a. Set **candidates** to be the subset of the current **candidates** that have exactly the best performance of any individual currently in **candidates** for the first case in **cases**.
    b. If **candidates** contains just a single individual then return it.
    c. If **case** contains just a single test case then return a randomly selected individual from **candidates**.
    d. Otherwise remove the first case from **cases** and go to Loop.

[Ref1]_


For more information about Lexicase selection, and its benefits, see the following publications:

- `Solving Uncompromising Problems with Lexicase Selection <http://faculty.hampshire.edu/lspector/pubs/lexicase-IEEE-TEC.pdf>`_
- `Lexicase selection for program synthesis: a diversity analysis <http://cs.wlu.edu/~helmuth/Pubs/2015-GPTP-lexicase-diversity-analysis.pdf>`_
- `The Impact of Hyperselection on Lexicase Selection <http://cs.wlu.edu/~helmuth/Pubs/2016-GECCO-hyperselection.pdf>`_


Epsilon Lexicase Selection
""""""""""""""""""""""""""

Lexicase selection generally performs poorly on problems that use continuous outpus, such as regression. Epsilon Lexicase Selection is a form of lexicase selection that allows candidates to pass a test case as long as their error is within *epsilon* of the error of the best candidate on the test case. This change dramatically increases the performance of lexicase selection on regression problems. For an example of this, see the :doc:`Sextic (symbolic regression) example problem <Sextic>`.

For more information about Epsilon Lexicase selection, and its benefits, see the following publication:

- `Epsilon-lexicase selection for regression <http://www.williamlacava.com/pubs/GECCO_lex_reg_preprint.pdf>`_

Tournament Selection
""""""""""""""""""""

Tournament selection involved selecting the individual with the lowest total error from a small, random subset of the population. This subset is called the tournament. Each time a selection event occurs, a new random subset of the population is placed into the tournament.

Source Code
"""""""""""

The source code for all selection methods can be found in `this file <https://github.com/erp12/Pysh/blob/master/pysh/gp/selection.py>`_ on the Pysh Github.

Mutation
========

Mutation operators randomly modify a single parent to create new individuals. These modifications usually invlove inserting random code, or removing random parts of the parent. 

Uniform Mutation
""""""""""""""""

Uniformly mutates individual. For each token in genome, there is *uniform_mutation_rate* probability of being mutated. If a token is to be mutated, it has a uniform_mutation_constant_tweak_rate probability of being mutated using a constant mutator (which varies depending on the type of the token), and otherwise is replaced with a random instruction.

Uniform Close Mutation
""""""""""""""""""""""

Uniformly mutates the *close* markers in the individual's plush genes. Each *close* will have a *uniform_close_mutation_rate* probability of being changed, and those that are changed have a *close_increment_rate* chance of being incremented, and are otherwise decremented.

.. note::
	Pysh's mutation operators are likely to change. Uniform mutation will be split into multiple more specific mutators. Each of these mutation operators will have their tunable probability. 

Recombination (Crossover)
=========================

Recombination operators typically use 2 or more parents. Unlike mutation, the resulting individual is composed entirely of parts of the parents.

Alternation
"""""""""""

Uniformly alternates between the two parent plush genomes


Adding Additional Operators
===========================

Coming soon ... 

If you write your own genetic operator, I would love to hear about it! Also, I would strongly encourage you to submit a `Pull Request on Github <https://github.com/erp12/Pysh/pulls>`_.

------------



.. [Ref1] `Solving Uncompromising Problems with Lexicase Selection <http://faculty.hampshire.edu/lspector/pubs/lexicase-IEEE-TEC.pdf>`_