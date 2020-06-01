import pytest

from pyshgp.push.atoms import Input
from pyshgp.push.interpreter import DEFAULT_INTERPRETER
from pyshgp.push.state import PushState
from tests.push.instruction_test_specs import SPECS


def test_instructions(core_type_lib, push_config):
    iset = DEFAULT_INTERPRETER.instruction_set
    for spec in SPECS:
        in_state = PushState.from_dict(spec["in"], core_type_lib, push_config)
        ex_state = PushState.from_dict(spec["ex"], core_type_lib, push_config)
        DEFAULT_INTERPRETER.state = in_state
        instruction_name = spec["instr"]
        print(instruction_name, in_state, ex_state)
        DEFAULT_INTERPRETER.evaluate_atom(iset[instruction_name].meta(), push_config)
        ac_state = DEFAULT_INTERPRETER.state
        # ac_state.pretty_print()
        # print("---")
        # ex_state.pretty_print()
        # print()
        # print()
        assert ex_state == ac_state


def test_inputs(core_type_lib, push_config):
    in_state = PushState.from_dict({"inputs": [7, "x"], "int": []}, core_type_lib, push_config)
    ex_state = PushState.from_dict({"inputs": [7, "x"], "int": [7]}, core_type_lib, push_config)
    DEFAULT_INTERPRETER.state = in_state
    DEFAULT_INTERPRETER.evaluate_atom(Input(input_index=0), push_config)
    ac_state = DEFAULT_INTERPRETER.state
    assert ex_state == ac_state
    assert len(in_state.inputs) == 2

    in_state = PushState.from_dict({"inputs": [7, "x"], "str": []}, core_type_lib, push_config)
    ex_state = PushState.from_dict({"inputs": [7, "x"], "str": ["x"]}, core_type_lib, push_config)
    DEFAULT_INTERPRETER.state = in_state
    DEFAULT_INTERPRETER.evaluate_atom(Input(input_index=1), push_config)
    ac_state = DEFAULT_INTERPRETER.state
    assert ex_state == ac_state
    assert len(in_state.inputs) == 2
