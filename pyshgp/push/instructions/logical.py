"""Definitions for all core logical instructions."""
import operator as op
from typing import Tuple

from pyshgp.push.instruction import SimpleInstruction


def _and(a: bool, b: bool) -> Tuple[bool]:
    return a and b,


def _or(a: bool, b: bool) -> Tuple[bool]:
    return a or b,


def _not(a: bool) -> Tuple[bool]:
    return not a,


def _xor(a: bool, b: bool) -> Tuple[bool]:
    return op.xor(a, b),


def _invert_first_then_and(a: bool, b: bool) -> Tuple[bool]:
    return (not a) and b,


def _invert_second_then_and(a: bool, b: bool) -> Tuple[bool]:
    return a and (not b),


def _bool_from_int(i: int) -> Tuple[bool]:
    return bool(i),


def _bool_from_float(f: float) -> Tuple[bool]:
    return bool(f),


def instructions():
    """Return all core numeric instructions."""
    i = []

    i.append(SimpleInstruction(
        "bool_and",
        _and,
        input_stacks=["bool", "bool"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring="Pushes the result of and-ing the top two booleans."
    ))

    i.append(SimpleInstruction(
        "bool_or",
        _or,
        input_stacks=["bool", "bool"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring="Pushes the result of or-ing the top two booleans."
    ))

    i.append(SimpleInstruction(
        "bool_not",
        _not,
        input_stacks=["bool"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring="Pushes the inverse of the boolean."
    ))

    i.append(SimpleInstruction(
        "bool_xor",
        _xor,
        input_stacks=["bool", "bool"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring="Pushes the result of xor-ing the top two booleans."
    ))

    i.append(SimpleInstruction(
        "bool_invert_first_then_and",
        _invert_first_then_and,
        input_stacks=["bool", "bool"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring=""""Pushes the result of and-ing the top two booleans after inverting the
        top boolean."""
    ))

    i.append(SimpleInstruction(
        "bool_second_first_then_and",
        _invert_second_then_and,
        input_stacks=["bool", "bool"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring=""""Pushes the result of and-ing the top two booleans after inverting the
        second boolean."""
    ))

    i.append(SimpleInstruction(
        "bool_from_int",
        _bool_from_int,
        input_stacks=["int"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring="If the top int is 0, pushes False. Pushes True for any other int value."
    ))

    i.append(SimpleInstruction(
        "bool_from_float",
        _bool_from_float,
        input_stacks=["float"],
        output_stacks=["bool"],
        code_blocks=0,
        docstring="If the top float is 0.0, pushes False. Pushes True for any other float value."
    ))

    return i
