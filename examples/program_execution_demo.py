from __future__ import absolute_import, division, print_function, unicode_literals

import sys
from pysh.gp import gp
import pysh.pysh_globals as g
import pysh.pysh_interpreter as interp
import pysh.instruction as instr

# Depending on which version of python is being used,
# change record with function gets user input.
inpt = None
if sys.version_info[0] == 3:
    inpt = input
else: # Python 2
    inpt = raw_input

print("This script will demonstrate the execution of")
print("various programs that are solutions to the")
print("benchmark problems.")

# The list of possible programs to demo.
# ("name", [program], [inputs])
programs = [("odd", [instr.Pysh_Input_Instruction(0), 2, '_integer_mod', 1, '_integer_eq'], [3]),
			("rswn", [g.Character(" "), instr.Pysh_Input_Instruction(0), g.Character("\n"), '_string_replace_char', '_print_string', g.Character(" "), instr.Pysh_Input_Instruction(0), '_string_remove_char', '_char_all_from_string', '_char_stack_depth'], ["Hello Push GP!"]),
			("string_demo", [instr.Pysh_Input_Instruction(0), '_integer_stack_depth', '_integer_dup', '_integer_stack_depth', '_integer_sub', '_string_head', '_string_dup', '_string_concat'], ["abcdefg"]),
			("sextic", [instr.Pysh_Input_Instruction(0), instr.Pysh_Input_Instruction(0), '_float_dup', '_float_mult', '_float_div', instr.Pysh_Input_Instruction(0), instr.Pysh_Input_Instruction(0), '_float_mult', '_float_add', instr.Pysh_Input_Instruction(0), '_float_swap', '_float_dup', '_float_mult', '_float_mult', '_float_mult'], [1.23]),
			("2-bit controlled shift register", [instr.Pysh_Input_Instruction(2), '_exec_shove', [instr.Pysh_Input_Instruction(1)], instr.Pysh_Input_Instruction(0)], [1, 0, 1])]

# Print possible programs to demo
print()
print("number, problem name, program")
for i in list(range(len(programs))):
	print(i, programs[i][0])

# Get user input, and load corrisponding program
prog_index = int(inpt("Which program would you like to run? Enter the number. "))
prog_lst = programs[prog_index][1]
prog_inputs = programs[prog_index][2]
program = gp.load_program_from_list(prog_lst)

print()
print("The following program will be executed:")
print()
print(prog_lst)
print()
print("With the following inputs:")
print()
print(prog_inputs)
print()

print_trace = inpt("Would you like to see the program evalution step-by-step? [Y/n]")
print()
if print_trace == "" or print_trace.lower() == "y":
	print_trace = True
else:
	print_trace = False

# Create push interpreter and push inputs onto the _input stack.
interpreter = interp.Pysh_Interpreter()
for i in prog_inputs:
	interpreter.state.stacks['_input'].push_item(i)

# Run the push program
interpreter.run_push(program, print_trace)

print()
print("Final push state:")
print(interpreter.state.pretty_print())