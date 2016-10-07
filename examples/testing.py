from __future__ import absolute_import, division, print_function, unicode_literals

from pysh import pysh_interpreter as interp
from pysh.gp import gp


prog_lst = [3, ['_exec_do*times', '_integer_empty']]
program = gp.load_program_from_list(prog_lst)

interpreter = interp.Pysh_Interpreter()
interpreter.reset_pysh_state()
interpreter.run_push(program, True)

# f = lambda x: x * x
# f.__repr__ = "My Lambda Func (repr)"
# f.__str__ = "My Lambda Func (str)"
# print(f)
# print(repr(f))
# print(f(4))
# print(f.__str__)