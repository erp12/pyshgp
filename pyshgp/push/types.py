"""The ``types`` module contains the core PushTypes and functions to reference them.

A PushType simply is a named collection of Python and Numpy types. A PushType
can be used to determine if multiple items should be considered the same type
during Push program execution.

"""

from typing import Any, Tuple, Optional

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

    Attributes
    ----------
    name : str
        A name for the type. Used when referencing the PushType in Instruction
        definitions and will be the key in the PushState for the corresponding
        PushStack.
    underlying : Tuple[type]
        A tuple of python (or numpy) types that correspond to the underlying
        native types which the PushType is representing.

    """

    def __init__(self, name: str, underlying: Tuple[type]):
        self.name = name
        self.underlying = underlying

    def is_instance(self, thing: Any) -> bool:
        """Return true if thing is instance of PushTypes underlying type(s)."""
        return isinstance(thing, self.underlying)

    def coerce(self, thing: Any):
        """Convert thing into PushTypes underlying type."""
        try:
            return self.underlying[0](thing)
        except ValueError:
            raise PushError.failed_coerce(thing, self)

    def __repr__(self):
        return self.name + "<" + ",".join([t.__name__ for t in list(self.underlying)]) + ">"

    def __eq__(self, other):
        if not isinstance(other, PushType):
            return False
        return self.name == other.name and self.underlying == other.underlying

    def __hash__(self):
        return (self.name + str(self.underlying[0])).__hash__()


class _PushIntType(PushType):

    def __init__(self):
        super().__init__("int", (int, np.int32, np.int64))


class _PushFloatType(PushType):

    def __init__(self):
        super().__init__("float", (float, np.float32, np.float64))


class _PushStrType(PushType):

    def __init__(self):
        super().__init__("str", (str, np.str_))


class _PushBoolType(PushType):

    def __init__(self):
        super().__init__("bool", (bool, np.bool_,))


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


class _PushCharType(PushType):
    """The Character PushType."""

    def __init__(self):
        super().__init__("char", (Char, ))


# @TODO: Add vector type(s)


PushInt = _PushIntType()
PushFloat = _PushFloatType()
PushStr = _PushStrType()
PushBool = _PushBoolType()
PushChar = _PushCharType()

PUSH_TYPES = [PushBool, PushInt, PushChar, PushFloat, PushStr]

_type_lookup = dict([(t.name, t) for t in PUSH_TYPES])


def push_type_by_name(push_type_name: str) -> Optional[PushType]:
    """Return the PushType with given name. If not exits, return None."""
    return _type_lookup.get(push_type_name)


def push_type_of(thing: Any) -> Optional[PushType]:
    """Return the PushType of the given thing."""
    for push_type in PUSH_TYPES:
        if push_type.is_instance(thing):
            return push_type
    return None


def push_type_for_type(t: type) -> Optional[PushType]:
    """Return the PushType of the given python (or numpy) type."""
    for push_type in PUSH_TYPES:
        if t in push_type.underlying:
            return push_type
    return None
