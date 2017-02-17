from __future__ import absolute_import, division, print_function, unicode_literals 

from pyshgp import utils as u
from pyshgp import exceptions as e
import pyshgp.push.instruction as instr

from .. import instructions_test as i_t

inpt_valid = instr.PyshInputInstruction(1)
inpt_too_big = instr.PyshInputInstruction(7)
inpt_negative = instr.PyshInputInstruction(-1)

vote_float = instr.PyshClassVoteInstruction(1, '_float')
vote_int = instr.PyshClassVoteInstruction(1, '_integer')
vote_too_big = instr.PyshClassVoteInstruction(1, '_float')
vote_negative = instr.PyshClassVoteInstruction(-1, '_float')
vote_bad_type_1 = instr.PyshClassVoteInstruction(1, '_string')
vote_bad_type_2 = instr.PyshClassVoteInstruction(1, 'abc')


io_tests = [
	# _input#
	[{'_input' : ['A', 'B', 'C']}, inpt_valid, {'_input' : ['A', 'B', 'C'], '_string' : ['B']}],
	[{'_input' : ['A', 'B', 'C']}, inpt_too_big, e.InvalidInputStackIndex],
	[{'_input' : ['A', 'B', 'C']}, inpt_negative, e.InvalidInputStackIndex],
	# _classVote#
	### [{'_float' : [1.23]}, vote_float, {'_output' : ['', 1.23]}],
	### [{'_float' : [4]}, vote_int, {'_output' : ['', 4]}],
	# _print_[type]
	[{'_integer' : [7]}, '_print_integer', {'_output' : ['7']}],
	# _print_newline
	[{}, '_print_newline', {'_output' : ['\n']}],
	]

for t in io_tests:
	passed = i_t.run_test(t, True)
	if not passed:
		raise Exception("The following test failed: " + str(t))
print("All IO instructions passed.")