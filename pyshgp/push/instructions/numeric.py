"""Definitions for all core numeric instructions."""
import math

from pyshgp.push.instruction import SimpleInstruction
from pyshgp.utils import Token


def _add(a, b):
    return b + a,


def _sub(a, b):
    return b - a,


def _mult(a, b):
    return b * a,


def _p_div(a, b):
    if a == 0:
        return Token.revert
    return b / a,


def _p_mod(a, b):
    if a == 0:
        return Token.revert
    return b % a,


def _min(a, b):
    return min(a, b),


def _max(a, b):
    return max(a, b),


def _inc(x):
    return x + 1,


def _dec(x):
    return x - 1,


def _lt(a, b):
    return b < a,


def _gt(a, b):
    return b > a,


def _lte(a, b):
    return b <= a,


def _gte(a, b):
    return b >= a,


def _sin(x):
    return math.sin(x),


def _cos(x):
    return math.cos(x),


def _tan(x):
    return math.tan(x),


def _to_int(x):
    return int(x),


def _to_float(x):
    return float(x),


def instructions():
    """Return all core numeric instructions."""
    i = []

    for push_type in ["int", "float"]:
        i.append(SimpleInstruction(
            "{t}_add".format(t=push_type),
            _add,
            input_stacks=[push_type, push_type],
            output_stacks=[push_type],
            code_blocks=0,
            docstring="Adds the top two {t}s and pushes the result.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_sub".format(t=push_type),
            _sub,
            input_stacks=[push_type, push_type],
            output_stacks=[push_type],
            code_blocks=0,
            docstring="Subtracts the top two {t}s and pushes the result.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_mult".format(t=push_type),
            _mult,
            input_stacks=[push_type, push_type],
            output_stacks=[push_type],
            code_blocks=0,
            docstring="Multiplies the top two {t}s and pushes the result.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_div".format(t=push_type),
            _p_div,
            input_stacks=[push_type, push_type],
            output_stacks=[push_type],
            code_blocks=0,
            docstring="Divides the top two {t}s and pushes the result.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_mod".format(t=push_type),
            _p_mod,
            input_stacks=[push_type, push_type],
            output_stacks=[push_type],
            code_blocks=0,
            docstring="Computes the modulus of the top two {t}s and pushes the result.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_min".format(t=push_type),
            _min,
            input_stacks=[push_type, push_type],
            output_stacks=[push_type],
            code_blocks=0,
            docstring="Pushes the minimum of two {t}.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_max".format(t=push_type),
            _max,
            input_stacks=[push_type, push_type],
            output_stacks=[push_type],
            code_blocks=0,
            docstring="Pushes the maximum of two {t}.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_inc".format(t=push_type),
            _inc,
            input_stacks=[push_type],
            output_stacks=[push_type],
            code_blocks=0,
            docstring="Increments the top {t} by 1.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_dec".format(t=push_type),
            _dec,
            input_stacks=[push_type],
            output_stacks=[push_type],
            code_blocks=0,
            docstring="Decrements the top {t} by 1.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_lt".format(t=push_type),
            _lt,
            input_stacks=[push_type, push_type],
            output_stacks=["bool"],
            code_blocks=0,
            docstring="Pushes true if the top {t} is less than the second. Pushes false otherwise.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_lte".format(t=push_type),
            _lte,
            input_stacks=[push_type, push_type],
            output_stacks=["bool"],
            code_blocks=0,
            docstring="Pushes true if the top {t} is less than, or equal to, the second. Pushes false otherwise.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_gt".format(t=push_type),
            _gt,
            input_stacks=[push_type, push_type],
            output_stacks=["bool"],
            code_blocks=0,
            docstring="Pushes true if the top {t} is greater than the second.. Pushes false otherwise.".format(t=push_type)
        ))

        i.append(SimpleInstruction(
            "{t}_gte".format(t=push_type),
            _gte,
            input_stacks=[push_type, push_type],
            output_stacks=["bool"],
            code_blocks=0,
            docstring="Pushes true if the top {t} is greater than, or equal to, the second. Pushes false otherwise.".format(t=push_type)
        ))

    # Trig functions

    i.append(SimpleInstruction(
        "float_sin",
        _sin,
        input_stacks=["float"],
        output_stacks=["float"],
        code_blocks=0,
        docstring="Pushes the sin of the top float."
    ))

    i.append(SimpleInstruction(
        "float_cos",
        _cos,
        input_stacks=["float"],
        output_stacks=["float"],
        code_blocks=0,
        docstring="Pushes the cos of the top float."
    ))

    i.append(SimpleInstruction(
        "float_tan",
        _tan,
        input_stacks=["float"],
        output_stacks=["float"],
        code_blocks=0,
        docstring="Pushes the tan of the top float."
    ))

    # Type converting

    i.append(SimpleInstruction(
        "int_from_bool",
        _to_int,
        input_stacks=["bool"],
        output_stacks=["int"],
        code_blocks=0,
        docstring="Pushes 1 in the top boolean is true. Pushes 0 if the top boolean is false."
    ))

    i.append(SimpleInstruction(
        "float_from_bool",
        _to_float,
        input_stacks=["bool"],
        output_stacks=["float"],
        code_blocks=0,
        docstring="Pushes 1.0 in the top boolean is true. Pushes 0.0 if the top boolean is false."
    ))

    i.append(SimpleInstruction(
        "int_from_float",
        _to_int,
        input_stacks=["float"],
        output_stacks=["int"],
        code_blocks=0,
        docstring="Casts the top float to an integer and pushes the result."
    ))

    i.append(SimpleInstruction(
        "float_from_int",
        _to_float,
        input_stacks=["int"],
        output_stacks=["float"],
        code_blocks=0,
        docstring="Casts the top integer to a float and pushes the result."
    ))

    return i
