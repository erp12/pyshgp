import sys
from .. import pysh_globals as g
from .. import utils as u

from ..instructions import boolean, char, code, common, numbers, string, input_output
from ..instructions import registered_instructions 

default_evolutionary_params = {
"error_threshold" : 0, # If any total error of individual is below this, that is considered a solution
"population_size" : 1000, # Size of the population at each generation
"max_generations" : 1000, # Max generations before evoluion stops. Will stop sooner if solution is found
"max_genome_initial_size" : 50, # Maximum size of random genomes generated for initial population
"max_points" : 200, # Maximum size of push genomes and push programs, as counted by points in the program. <- Might not be implemented correctly yet

# The instructions that pushgp will use in random code generation
"atom_generators" : u.merge_dicts(registered_instructions.registered_instructions,
                                  {"f1" : lambda: random.randint(0, 100),
                                   "f2" : lambda: random.random()}),

# Probabilities of parents from previous generation undergoing each
# genetic operators to produce a child.
# More coming soon!
"genetic_operator_probabilities" : {"alternation" : 0.7,
                                    "uniform_mutation" : 0.1,
                                    "alternation & uniform_mutation" : 0.2,
                                    "uniform_close_mutation" : 0.0},

#############
# SELECTION #
#############
"selection_method" : "lexicase", # Options are 'lexicase', 'epsilon_lexicase', 'cluster_lexicase' or tournament';

# Arguments related to lexicase selection, and its variants
"epsilon_lexicase_epsilon" : None, # Defines a hard-coded epsilon. If None, automaticly defines epsilon using MAD.
"cluster_lexicase_clusters" : 10,

# Arguments related to Tournament Selection
"tournament_size" : 7, # If using tournament selection, the size of the tournaments

###########################
# CROSSOVER & ALTERNATION #
###########################

# Arguments related to alternation
"alternation_rate" : 0.01, # When using alternation, how often alternates between the parents
"alignment_deviation" : 10, # When using alternation, the standard deviation of how far alternation may jump between indices when switching between parents

############
# MUTATION #
############

# Arguments related to uniform mutation
"uniform_mutation_rate" : 0.01, # The probability of each token being mutated during uniform mutation
"uniform_mutation_constant_tweak_rate" : 0.5, # The probability of using a constant mutation instead of simply replacing the token with a random instruction during uniform mutation
"uniform_mutation_float_gaussian_standard_deviation" : 1.0, # The standard deviation used when tweaking float constants with Gaussian noise
"uniform_mutation_int_gaussian_standard_deviation" : 1, # The standard deviation used when tweaking integer constants with Gaussian noise
"uniform_mutation_string_char_change_rate" : 0.1,

# Arguments related to uniform close mutation
"uniform_close_mutation_rate" : 0.1, # The probability of each :close being incremented or decremented during uniform close mutation.
"close_increment_rate" : 0.2, # The probability of making an increment change to :close during uniform close mutation, as opposed to a decrement change.

# Epignenetics
"epigenetic_markers" : ["_close"], # A vector of the epigenetic markers that should be used in the individuals. Implemented options include: :close, :silent
"close_parens_probabilities" : [0.772, 0.206, 0.021, 0.001], # A vector of the probabilities for the number of parens ending at that position.         
"silent_instruction_probability" : 0.2, # If :silent is used as an epigenetic-marker, this is the probability of random instructions having :silent be true

# Program Simplification
"final_simplification_steps" : 5000, # The number of simplification steps that will happen upon finding a solution.

# Monitoring Evolution
"things_to_monitor" : {"best_total_error" : True,
                       "average_total_error" : True,
                       "average_genome_size" : True,
                       "smallest_genome_size" : True,
                       "largest_genome_size" : True,
                       "unique_program_count" : True,
                       "unique_error_vectors" : True,
                       "best_program_by_total_error" : True},
# Send SMS every few x generations. 0 means never send text.
"SMS_every_x_generations" : None,

# End of run plots
"reports" : {"timings" : True,
             "plot_piano_roll" : False,
             "final_SMS" : False},

#
"max_workers" : None, # If 1, pysh runs in single thread. Otherwise, pysh runs in parrell. If None, uses number of cores on machine.
"parallel_evaluation" : True,
"parallel_genetics" : False
}

def safe_cast_arg(arg, typ = int):
    if typ == int or typ == float:
        try:
            return typ(arg)
        except Exception as e:
            if typ == int:
                return safe_cast_arg(arg, float)
            elif typ == float:
                return safe_cast_arg(arg, bool)
    else:
        if arg == 'True':
            return True
        elif arg == 'False':
            return False
        return str(arg)

def grab_command_line_params(evolutionary_params):
    '''
    Loads parameters from command line and overwrites the problem specific / default
    parameter values.
    '''
    i = 0
    while i < len(sys.argv):
        i_s = 1
        if sys.argv[i].startswith('-'):
            k_s = [sys.argv[i][1:]]
            j = 1
            while sys.argv[i+j].startswith('-'):
                k_s.append(sys.argv[i+j][1:])
                j += 1
                i_s +=1
            v = safe_cast_arg(sys.argv[i+j])
            d = evolutionary_params
            for key in k_s[:-1]:
                d = evolutionary_params[key]
            d[k_s[-1]] = v
        i += i_s

def init_executor(evolutionary_params):
    from pathos.multiprocessing import ProcessingPool as Pool

    if evolutionary_params["max_workers"] == None:
        evolutionary_params["pool"] = Pool()
    else:
        evolutionary_params['pool'] = Pool(evolutionary_params["max_workers"])

def setup_SMS(evolutionary_params):
    print("Preparing to send text updates")
    from .. import text_me
    if sys.version_info[0] == 3:
        evolutionary_params['run_name'] = input("Enter a name for this run: ")
    else: # Python 2
        evolutionary_params['run_name'] = raw_input("Enter a name for this run: ")




