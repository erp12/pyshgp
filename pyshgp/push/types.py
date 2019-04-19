"""The ``types`` module contains the core PushTypes and functions to reference them.

A PushType simply is a named collection of Python types. A PushType
can be used to determine if multiple items should be considered the same type
during Push program execution.

"""
from typing import Any, Tuple, Callable, Optional

import numpy as np

from pyshgp.validation import PushError


class PushType:
    """Type information for values used by Push programs.

    Parameters
    ----------
    name : str
        A name for the type. Used when referencing the PushType in Instruction
        definitions and will be the key in the PushState for the corresponding
        PushStack.
    underlying : Tuple[type]
        A tuple of python (or numpy) types that correspond to the underlying
        native types which the PushType is representing.
    coercion_func : Callable[[Any], Any], optional
        A function which takes a single argument and returns argument coerced
        into the PushTypes canonical type (the first type in ``underlying``).
        If None, the constructor of the canonical type is used. Default is None.

    Attributes
    ----------
    name : str
        A name for the type. Used when referencing the PushType in Instruction
        definitions and will be the key in the PushState for the corresponding
        PushStack.
    underlying : Tuple[type]
        A tuple of python (or numpy) types that correspond to the underlying
        native types which the PushType is representing.
    coercion_func : Callable[[Any], Any], optional
        A function which takes a single argument and returns argument coerced
        into the PushTypes canonical type (the first type in ``underlying``).
        If None, the constructor of the canonical type is used. Default is None.

    """

    def __init__(self, name: str, underlying: Tuple[type], coercion_func: Optional[Callable[[Any], Any]] = None):
        self.name = name
        self.underlying = underlying
        if coercion_func is None:
            self.coercion_func = underlying[0]
        else:
            self.coercion_func = coercion_func

    def is_instance(self, thing: Any) -> bool:
        """Return true if thing is instance of PushTypes underlying type(s)."""
        return isinstance(thing, self.underlying)

    def coerce(self, thing: Any):
        """Convert thing into PushTypes underlying type."""
        try:
            return self.coercion_func(thing)
        except Exception as e:
            err_type = type(e).__name__
            err_msg = str(e)
            raise PushError(
                "{t} while coerceing {x} of {typ1} to {typ2}. Origional mesage: \"{m}\"".format(
                    t=err_type, x=thing, typ1=type(thing), typ2=self, m=err_msg
                )
            )

    def __repr__(self):
        return self.name + "<" + ",".join([t.__name__ for t in list(self.underlying)]) + ">"

    def __eq__(self, other):
        if not isinstance(other, PushType):
            return False
        return self.name == other.name and self.underlying == other.underlying

    def __hash__(self):
        return (self.name + str(self.underlying[0])).__hash__()


class Char(str):
    """Holds a string of length 1.

    Used to distinguish between string and char literals in Push program
    interpretation.

    Attributes
    ----------
    char : str
        String of length 1.

    """

    def __init__(self, char):
        if len(char) == 0:
            raise PushError.empty_character()
        if len(char) > 1:
            raise PushError.long_character()

    def __eq__(self, other):
        return isinstance(other, Char) and str(self) == str(other)


# @TODO: Add vector type(s)


PushInt = PushType("int", (int, np.int64, np.int32, np.int16, np.int8))
PushFloat = PushType("float", (float, np.float64, np.float32, np.float16))
PushStr = PushType("str", (str, np.str_))
PushBool = PushType("bool", (bool, np.bool_))
PushChar = PushType("char", (Char, ))

CORE_PUSH_TYPES = [PushBool, PushInt, PushChar, PushFloat, PushStr]
