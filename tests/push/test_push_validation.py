from pyshgp.push.interpreter import PushInterpreter, PushInterpreterStatus
from pyshgp.push.config import PushConfig
from pyshgp.push.program import ProgramSignature, Program
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.state import PushState
from tests.support import load_code, get_program


def check_program(name: str, inputs: list, outputs: list, sig: ProgramSignature, iset: InstructionSet) -> PushState:
    """Returns the PushState for further validation."""
    interpreter = PushInterpreter(iset)
    prog = get_program(name, sig, interpreter)
    assert interpreter.run(prog, inputs) == outputs
    return interpreter.state


def test_program_relu_1(push_config: PushConfig, instr_set: InstructionSet):
    name = "relu_via_max"
    sig = ProgramSignature(arity=1, output_stacks=["float"], push_config=push_config)
    check_program(name, [-5], [0.0], sig, instr_set)
    check_program(name, [5.6], [5.6], sig, instr_set)


def test_program_relu_2(push_config: PushConfig, instr_set: InstructionSet):
    name = "relu_via_if"
    sig = ProgramSignature(arity=1, output_stacks=["float"], push_config=push_config)
    check_program(name, [-5], [0.0], sig, instr_set)
    check_program(name, [5.6], [5.6], sig, instr_set)


def test_program_fibonacci(push_config: PushConfig, instr_set: InstructionSet):
    name = "fibonacci"
    sig = ProgramSignature(arity=1, output_stacks=[], push_config=push_config)
    result1 = check_program(name, [5], [], sig, instr_set)
    assert list(result1["int"]) == [1, 1, 2, 3, 5]
    result2 = check_program(name, [1], [], sig, instr_set)
    assert list(result2["int"]) == [1]
    result3 = check_program(name, [-2], [], sig, instr_set)
    assert list(result3["int"]) == []


def test_program_rswn(push_config: PushConfig, instr_set: InstructionSet):
    name = "replace_space_with_newline"
    sig = ProgramSignature(arity=1, output_stacks=["int", "stdout"], push_config=push_config)
    result1 = check_program(name, ["hello world"], [10, "hello\nworld"], sig, instr_set)
    assert result1.stdout == "hello\nworld"
    result2 = check_program(name, ["nospace"], [7, "nospace"], sig, instr_set)
    assert result2.stdout == "nospace"
    result3 = check_program(name, ["   "], [0, "\n\n\n"], sig, instr_set)
    assert result3.stdout == "\n\n\n"


def test_program_point_dist(push_config: PushConfig, point_instr_set: InstructionSet):
    name = "point_distance"
    sig = ProgramSignature(arity=4, output_stacks=["float"], push_config=push_config)
    check_program(name, [1.0, 3.0, 3.0, 3.0], [2.0], sig, point_instr_set)
    check_program(name, [3.0, 2.5, 3.0, -3.0], [5.5], sig, point_instr_set)
    check_program(name, [0.0, 0.0, 0.0, 0.0], [0], sig, point_instr_set)


def test_interpreter_constraints(push_config: PushConfig, instr_set: InstructionSet):
    name = "infinite_growth"
    sig = ProgramSignature(arity=0, output_stacks=["int"], push_config=push_config)
    interpreter = PushInterpreter(instr_set)
    cb = load_code(name, interpreter)
    program = Program(code=cb, signature=sig)
    output = interpreter.run(program, [0], print_trace=True)
    assert output[0] == int(push_config.numeric_magnitude_limit)
    assert interpreter.status == PushInterpreterStatus.step_limit_exceeded
