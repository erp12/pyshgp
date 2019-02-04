import pytest

from pyshgp.push.interpreter import DEFAULT_INTERPRETER, PushInterpreter
from pyshgp.push.state import PushState
from pyshgp.push.atoms import Literal
from pyshgp.push.instructions.io import make_input_instruction
from tests.push.instruction_test_specs import SPECS


def test_instructions():
    for spec in SPECS:
        in_state = PushState.from_dict(spec["in"])
        ex_state = PushState.from_dict(spec["ex"])
        DEFAULT_INTERPRETER.state = in_state
        print(spec["instr"], in_state, ex_state)
        DEFAULT_INTERPRETER.evaluate_atom(spec["instr"])
        ac_state = DEFAULT_INTERPRETER.state
        # ac_state.pretty_print()
        # print("---")
        # ex_state.pretty_print()
        # print()
        # print()
        assert ex_state == ac_state


def test_input_instructions():
    in_state = PushState.from_dict({"inputs": [7, "x"], "exec": []})
    ex_state = PushState.from_dict({"inputs": [7, "x"], "exec": [Literal(7)]})
    DEFAULT_INTERPRETER.state = in_state
    DEFAULT_INTERPRETER.evaluate_atom(make_input_instruction(0))
    ac_state = DEFAULT_INTERPRETER.state
    assert ex_state == ac_state
    assert len(in_state.inputs) == 2

    in_state = PushState.from_dict({"inputs": [7, "x"], "exec": []})
    ex_state = PushState.from_dict({"inputs": [7, "x"], "exec": [Literal("x")]})
    DEFAULT_INTERPRETER.state = in_state
    DEFAULT_INTERPRETER.evaluate_atom(make_input_instruction(1))
    ac_state = DEFAULT_INTERPRETER.state
    assert ex_state == ac_state
    assert len(in_state.inputs) == 2
