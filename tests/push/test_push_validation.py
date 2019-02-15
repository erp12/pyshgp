from pyshgp.push.atoms import CodeBlock
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet


# Not using fixture in order to spot unintentional updates during execution.
i_set = InstructionSet(register_all=True).register_n_inputs(10)


def load_program(name: str) -> CodeBlock:
    with open("tests/resources/programs/" + name + ".json") as f:
        return CodeBlock.from_json_str(f.read(), i_set)


def test_program_relu_1(interpreter: PushInterpreter):
    prog = load_program("relu_via_max")
    result = interpreter.run(prog, [-5], ["float"], verbose=True)
    assert result == [0.0]

    result = interpreter.run(prog, [5.6], ["float"], verbose=True)
    assert result == [5.6]


def test_program_relu_2(interpreter: PushInterpreter):
    prog = load_program("relu_via_if")
    result = interpreter.run(prog, [-5], ["float"], verbose=True)
    assert result == [0.0]

    result = interpreter.run(prog, [5.6], ["float"], verbose=True)
    assert result == [5.6]


def test_program_fibonacci(interpreter: PushInterpreter):
    prog = load_program("fibonacci")
    interpreter.run(prog, [5], [], verbose=True)
    assert list(interpreter.state["int"]) == [1, 1, 2, 3, 5]

    interpreter.run(prog, [1], [], verbose=True)
    assert list(interpreter.state["int"]) == [1]

    interpreter.run(prog, [-3], [], verbose=True)
    assert list(interpreter.state["int"]) == []


def test_program_rswn(interpreter: PushInterpreter):
    prog = load_program("replace_space_with_newline")
    interpreter.run(prog, ["hello world"], [], verbose=True)
    assert list(interpreter.state["int"]) == [10]
    assert interpreter.state.stdout == "hello\nworld"

    interpreter.run(prog, ["nospace"], [], verbose=True)
    assert list(interpreter.state["int"]) == [7]
    assert interpreter.state.stdout == "nospace"

    interpreter.run(prog, ["   "], [], verbose=True)
    assert list(interpreter.state["int"]) == [0]
    assert interpreter.state.stdout == "\n\n\n"
