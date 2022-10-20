import logging

import pytest

from pyshgp.push2 import Program, Block, Signature, Input, Lit, Instr

logging.getLogger().setLevel(logging.DEBUG)


def test_harmonic_mean():
    prog = Program(
        signature=Signature(
            inputs={"a": "float", "b": "float", "c": "float"}, outputs=("float",)
        ),
        code=Block(
            [
                # First term: 1/a
                Input("a"),
                Lit(1.0, "float"),
                Instr("float_div"),
                # First term: 1/b
                Input("b"),
                Lit(1.0, "float"),
                Instr("float_div"),
                # First term: 1/c
                Input("c"),
                Lit(1.0, "float"),
                Instr("float_div"),
                # Sum terms
                Instr("float_add"),
                Instr("float_add"),
                # Divide the number of terms by the sum
                Lit(3.0, "float"),
                Instr("float_div"),
            ]
        ),
    )
    assert prog(a=1.0, b=4.0, c=4.0) == (2.0,)
    assert prog(a=1.0, b=2.0, c=4.0) == pytest.approx((1.714286,))
