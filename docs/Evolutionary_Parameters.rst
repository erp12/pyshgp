.. sidebar:: Useful Links

	* `Evolutionary Parameters <Evolutionary_Parameters.html>`_
	* `Instruction Set <Instructions.html>`_
	* `Examples <Examples.html>`_

.. toctree::
   :maxdepth: 1

************************
Parameters For Evolution
************************

Setting Parameter Values
########################

Pysh supports 3 different ways to set the evolutionary parameters for a Pysh GP run.

1. Inside the problem file:
"""""""""""""""""""""""""""
	
A dictionary of problem specific values for evolutionary parameters can be set in the problem file, alongside the error function. This dictionary can overwrite the defaults of every evolutionary parameter, or only a subset. This diction is passed to the ``gp.evolution()`` function in the ``gp/gp.py`` file. Evolutionary parameters set in this way will be overwritten by corrisponding parameters passed from the command line.

For examples on how to do this, refer to the Pysh `examples <Examples.html>`_ documentation, such as `Odd <Odd.html>`_ and `Integer Regression <Integer_Regression>`_.

2. From the command line:
"""""""""""""""""""""""""

Pysh supports passing evolutionary parameters from the command line. To run the example `Odd <Odd.html>`_ problem with a population size of 777, the following command could be run::

	python odd.py --population_size=777

When setting evolutionary params in this way, each parameter must be set with its own flag. Each flag must start with two dashes and contain no spaces. Following the two dashes, each flag must have the parameter name, and equals sign, and the new value for the parameter in that order.

Setting parameters from the command line will overwrite Pysh default parameter values and paramters set in the problem file. They will also only be used on the one run which they were set for.
	

3. Change Pysh defaults:
""""""""""""""""""""""""

The dictionary of default evolutionary paramters exists in ``gp/gp.py``, and can be edited directly. This will change the default value of the parameter for all runs, of all problems. Parameters set in this way will be overwritten by problem file parameters, and command line arguments.


Parameter Descriptions
######################

error_threshold                                       
"""""""""""""""
If any total error of individual is below this, that is considered a solution.

population_size
"""""""""""""""
Size of the population at each generation.

max_generations
""""""""""""""""""""""""""""""""""""""""""""""""""
Max generations before evoluion stops. Will stop sooner if solution is found.

max_genome_initial_size
""""""""""""""""""""""""""""""""""""""""""""""""""
Maximum size of random genomes generated for initial population.

max_points
""""""""""""""""""""""""""""""""""""""""""""""""""
Maximum size of push genomes and push programs, as counted by points in the program.

atom_generators
""""""""""""""""""""""""""""""""""""""""""""""""""
The instructions that pushgp will use in random code generation.

genetic_operator_probabilities
""""""""""""""""""""""""""""""""""""""""""""""""""
Probabilities of parents from previous generation undergoing each genetic operators to produce a child. Options include *alternation* and *uniform crossover*.

selection_method
""""""""""""""""""""""""""""""""""""""""""""""""""
Defines the method of how parents are selected. Options are 'lexicase' or 'tournament'.

tournament_size
""""""""""""""""""""""""""""""""""""""""""""""""""
If using tournament selection, the size of the tournaments.

alternation_rate
""""""""""""""""""""""""""""""""""""""""""""""""""
When using alternation, how often alternates between the parents.

alignment_deviation
""""""""""""""""""""""""""""""""""""""""""""""""""
When using alternation, the standard deviation of how far alternation may jump between indices when switching between parents.

uniform_mutation_rate
""""""""""""""""""""""""""""""""""""""""""""""""""
The probability of each token being mutated during uniform mutation.

uniform_mutation_constant_tweak_rate
""""""""""""""""""""""""""""""""""""""""""""""""""
The probability of using a constant mutation instead of simply replacing the token with a random instruction during uniform mutation.

uniform_mutation_float_gaussian_standard_deviation
""""""""""""""""""""""""""""""""""""""""""""""""""
The standard deviation used when tweaking float constants with Gaussian noise.

uniform_mutation_int_gaussian_standard_deviation
""""""""""""""""""""""""""""""""""""""""""""""""""
The standard deviation used when tweaking integer constants with Gaussian noise.

epigenetic_markers
""""""""""""""""""""""""""""""""""""""""""""""""""
A vector of the epigenetic markers that should be used in the individuals. Implemented options include: _close, _silent.

close_parens_probabilities
""""""""""""""""""""""""""""""""""""""""""""""""""
A vector of the probabilities for the number of parens ending at that position.

silent_instruction_probability
""""""""""""""""""""""""""""""""""""""""""""""""""
If :silent is used as an epigenetic-marker, this is the probability of random instructions having :silent be true.

final_simplification_steps
""""""""""""""""""""""""""""""""""""""""""""""""""
The number of simplification steps that will happen upon finding a solution.

things_to_monitor
""""""""""""""""""""""""""""""""""""""""""""""""""
Dictionary of boolean values determining which metrics to print at each generations. Options include: average_total_error, average_genome_size, smallest_genome_size, largest_genome_size, unique_genome_count.

