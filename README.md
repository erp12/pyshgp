# Pysh2
Push Genetic Programming in Python. For the most complete documentation, refer to the [ReadTheDocs](http://pysh2.readthedocs.io/en/latest/index.html).

## Push Genetic Programming
Push is programming language that plays nice with evolutionay computing / genetic programming. It is a stack-based language that features 1 stack per data type, including code. Programs are represented by lists of instructions, which modify the values on the stacks. Instuctions are executed in order.

More information about PushGP can be found here: http://faculty.hampshire.edu/lspector/push.html

For the most cutting edge PushGP framework, see the [Clojure](https://clojure.org/) implementaion called [Clojush](https://github.com/lspector/Clojush).

## How to Use Pysh2

### Example Usage
To try the odd example, run `python -m pysh.problems.odd` in the directory above the pysh directory.

Odd problem source:
```python
import copy
import random

from ..gp import gp
from .. import pysh_interpreter
from ..instructions import *
from ..instructions import registered_instructions 

'''
This problem evolves a program to determine if a number is odd or not.
'''

def odd_error_func(program):
	errors = []

	for i in range(9):
		prog = copy.deepcopy(program)
		# Create the push interpreter
		interpreter = pysh_interpreter.Pysh_Interpreter()
		interpreter.reset_pysh_state()
		
		# Push input number		
		interpreter.state.stacks["_integer"].push_item(i)
		interpreter.state.stacks["_input"].push_item(i)

		# Run program
		interpreter.run_push(prog)
		# Get output
		prog_output = interpreter.state.stacks["_boolean"].stack_ref(0)
		#compare to target output
		target_output = bool(i % 2)

		if prog_output == target_output:
			errors.append(0)
		else:
			errors.append(1)

	return errors
	
odd_params = {
"atom_generators" : registered_instructions.registered_instructions +	# Use all possible instructions,
                      [lambda: random.randint(0, 100),					# and some integers
                       lambda: random.random(),							# and some floats
                       "_in1"]}											# and an input instruction that pushes the input to the _integer stack.

if __name__ == "__main__":
	gp.evolution(odd_error_func, odd_params)
```

More demonstrations of this can be found on [Pysh's ReadTheDocs page](http://pysh2.readthedocs.io/en/latest/index.html).


## Current State of Pysh2

Pysh2 is currently under active development.
Feel free to submit a pull request if you have any additions to make.

#### In Progress Features
-	More complete string instructions
-   Add string mutation to Uniform Mutation algorithm
-	More benchmark problems
-	Utility functions to filter registered instructions by type

#### Future Features
-	Add parallel evaluation
-	Add compatibility with python 3

