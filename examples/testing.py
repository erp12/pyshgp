from __future__ import absolute_import, division, print_function, unicode_literals

from pysh import pysh_interpreter as interp
from pysh import utils as u
from pysh.gp import gp


prog_lst = [7, '_char_from_integer']
program = gp.load_program_from_list(prog_lst)

interpreter = interp.Pysh_Interpreter()
interpreter.reset_pysh_state()
interpreter.run_push(program, True)
