"""Definitions for all core I/O instructions, including input instructions."""
from typing import Sequence
from functools import partial

from pyshgp.push.state import PushState
from pyshgp.push.atoms import Atom
from pyshgp.push.instruction import SimpleInstruction, TakesStateInstruction
from pyshgp.push.type_library import PushTypeLibrary


# Printing instructions

def _wrap_str(x):
    return str(x),


def instructions(type_library: PushTypeLibrary):
    """Return all core printing instructions."""
    i = []

    for push_type in type_library.keys():
        i.append(SimpleInstruction(
            "print_{t}".format(t=push_type),
            _wrap_str,
            input_stacks=[push_type],
            output_stacks=["stdout"],
            code_blocks=0,
            docstring="Prints the top {t}.".format(t=push_type)
        ))
    return i
