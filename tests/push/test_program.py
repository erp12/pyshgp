from pyshgp.push.config import PushConfig
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.program import ProgramSignature
from tests.support import get_program


class TestPrettyString:

    def test_relu_1(self, push_config: PushConfig, interpreter: PushInterpreter):
        name = "relu_via_max"
        sig = ProgramSignature(arity=1, output_stacks=["float"], push_config=push_config)
        prog = get_program(name, sig, interpreter)
        assert prog.pretty_str() == "(input_0 float_from_int 0.0 float_max)"

    def test_relu_2(self, push_config: PushConfig, interpreter: PushInterpreter):
        name = "relu_via_if"
        sig = ProgramSignature(arity=1, output_stacks=["float"], push_config=push_config)
        prog = get_program(name, sig, interpreter)
        assert prog.pretty_str() == "(input_0 float_from_int 0.0 float_gt exec_if (input_0) (0.0))"

    def test_fibonacci(self, push_config: PushConfig, interpreter: PushInterpreter):
        name = "fibonacci"
        sig = ProgramSignature(arity=1, output_stacks=["float"], push_config=push_config)
        prog = get_program(name, sig, interpreter)
        assert prog.pretty_str() == "(input_0 0 int_lte exec_when (exec_flush) 1 input_0 2 int_min int_dup_times input_0 2 int_lte exec_when (exec_flush) input_0 2 int_sub exec_do_times (int_dup 2 int_yank_dup int_add))"

    def test_replace_space_with_newline(self, push_config: PushConfig, interpreter: PushInterpreter):
        name = "replace_space_with_newline"
        sig = ProgramSignature(arity=1, output_stacks=["float"], push_config=push_config)
        prog = get_program(name, sig, interpreter)
        assert prog.pretty_str() == "(input_0 \"\n\" \" \" str_replace_all_char print_str input_0 input_0 \" \" str_remove_all_char str_length)"

    def test_point_distance(self, push_config: PushConfig, point_instr_set: InstructionSet):
        name = "point_distance"
        sig = ProgramSignature(arity=4, output_stacks=["float"], push_config=push_config)
        interpreter = PushInterpreter(point_instr_set)
        prog = get_program(name, sig, interpreter)
        assert prog.pretty_str() == "(input_0 input_1 point_from_floats input_2 input_3 point_from_floats point_dist)"

    def test_infinite_growth(self, push_config: PushConfig, interpreter: PushInterpreter):
        name = "infinite_growth"
        sig = ProgramSignature(arity=1, output_stacks=["float"], push_config=push_config)
        prog = get_program(name, sig, interpreter)
        assert prog.pretty_str() == "(10 exec_dup (int_dup int_mult exec_dup))"
