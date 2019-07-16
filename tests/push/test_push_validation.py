import json

from pyshgp.push.atoms import CodeBlock, Closer, Literal, JitInstructionRef
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet


def _code_block_from_list(lst: list, instr_set: InstructionSet) -> CodeBlock:
    type_lib = instr_set.type_library
    cb = CodeBlock()
    for atom_spec in lst:
        atom = None
        if isinstance(atom_spec, list):
            atom = _code_block_from_list(atom_spec, instr_set)
        else:
            atom_type = atom_spec["a"]
            if atom_type == "close":
                atom = Closer()
            elif atom_type == "lit":
                push_type = type_lib[atom_spec["t"]]
                value = push_type.coerce(atom_spec["v"])
                atom = Literal(value, push_type)
            elif atom_type == "instr":
                atom = instr_set[atom_spec["n"]]
            elif atom_type == "jit-instr":
                atom = JitInstructionRef(atom_spec["n"])
            else:
                raise ValueError("bad atom spec {s}".format(s=atom_spec))
        cb.append(atom)
    return cb


def load_program(name, interpreter) -> CodeBlock:
    with open("tests/resources/programs/" + name + ".json") as f:
        return _code_block_from_list(json.load(f), interpreter.instruction_set)


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
