from __future__ import absolute_import, division, print_function, unicode_literals

from pysh import pysh_interpreter as interp
from pysh.gp import gp


prog_lst = [0, 1, '_exec_do*times', '_integer_inc']
program = gp.load_program_from_list(prog_lst)

interpreter = interp.Pysh_Interpreter()
interpreter.reset_pysh_state()
interpreter.run_push(program, True)