************************
Parameters For Evolution
************************

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

