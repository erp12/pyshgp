from pyshgp.push.atoms import CodeBlock
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet


def load_program(name, interpreter) -> CodeBlock:
    with open("tests/resources/programs/" + name + ".json") as f:
        return CodeBlock.from_json_str(f.read(), interpreter.instruction_set)


def test_program_relu_1():
    interpreter = PushInterpreter(InstructionSet(register_core=True).register_n_inputs(1))
    prog = load_program("relu_via_max", interpreter)
    result = interpreter.run(prog, [-5], ["float"])
    assert result == [0.0]

    result = interpreter.run(prog, [5.6], ["float"])
    assert result == [5.6]


def test_program_relu_2():
    interpreter = PushInterpreter(InstructionSet(register_core=True).register_n_inputs(1))
    prog = load_program("relu_via_if", interpreter)
    result = interpreter.run(prog, [-5], ["float"])
    assert result == [0.0]

    result = interpreter.run(prog, [5.6], ["float"])
    assert result == [5.6]


def test_program_fibonacci():
    interpreter = PushInterpreter(InstructionSet(register_core=True).register_n_inputs(1))
    prog = load_program("fibonacci", interpreter)
    interpreter.run(prog, [5], [])
    assert list(interpreter.state["int"]) == [1, 1, 2, 3, 5]

    interpreter.run(prog, [1], [])
    assert list(interpreter.state["int"]) == [1]

    interpreter.run(prog, [-3], [])
    assert list(interpreter.state["int"]) == []


def test_program_rswn():
    interpreter = PushInterpreter(InstructionSet(register_core=True).register_n_inputs(1))
    prog = load_program("replace_space_with_newline", interpreter)
    interpreter.run(prog, ["hello world"], [])
    assert list(interpreter.state["int"]) == [10]
    assert interpreter.state.stdout == "hello\nworld"

    interpreter.run(prog, ["nospace"], [])
    assert list(interpreter.state["int"]) == [7]
    assert interpreter.state.stdout == "nospace"

    interpreter.run(prog, ["   "], [])
    assert list(interpreter.state["int"]) == [0]
    assert interpreter.state.stdout == "\n\n\n"


def test_program_point_dist(point_instr_set):
    interpreter = PushInterpreter(point_instr_set)
    prog = load_program("point_distance", interpreter)
    interpreter.run(prog, [1.0, 3.0, 3.0, 3.0], ["float"])
    assert list(interpreter.state["float"]) == [2.0]

    interpreter.run(prog, [3.0, 2.5, 3.0, -3.0], ["float"])
    assert list(interpreter.state["float"]) == [5.5]
