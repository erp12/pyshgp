import pysh_random
import pysh_interpreter

import pysh_plush_translation as translate
import pysh_globals as g

gn = pysh_random.random_plush_genome(50)						# Generation a plush genome with a max size of 50
print "PLUSH GENOME:\n", gn
print

prog = translate.translate_plush_genome_to_push_program(gn)		# Translate plush genome to push program
print "PUSH PROGRAM:\n", prog
print

interpreter = pysh_interpreter.Pysh_Interpreter()				# Create instance of a Pysh_Interpreter.
interpreter.run_push(prog)										# Run program.
print "PROGRAM OUTPUT:"
interpreter.state.pretty_print()

