import pysh_random
import pysh_plush_translation as translate
import pysh_interpreter

from gp import gp

# gn = pysh_random.random_plush_genome(gp.evolutionary_params)						# Generation a plush genome with a max size of 50
# print "PLUSH GENOME:\n", gn
# print

#Tprog = translate.translate_plush_genome_to_push_program(gn)		# Translate plush genome to push program
prog = gp.load_program_from_list([9, 1, 2, '_integer_add'])
print "PUSH PROGRAM:\n", prog
print

interpreter = pysh_interpreter.Pysh_Interpreter()				# Create instance of a Pysh_Interpreter.
interpreter.run_push(prog, True)										# Run program.
print "PROGRAM OUTPUT:"
interpreter.state.pretty_print()

