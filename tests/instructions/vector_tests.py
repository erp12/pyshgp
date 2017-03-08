from __future__ import absolute_import, division, print_function, unicode_literals 

from pyshgp import utils as u

from .. import instructions_test as i_t

vector_tests = [
	# _pop
	
	]

for t in vector_tests:
	passed = i_t.run_test(t)
	if not passed:
		raise Exception("The following test failed: " + str(t))
print("All vector instructions passed.")