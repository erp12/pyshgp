"""The ``types`` module contains the core PushTypes and functions to reference them.

A PushType simply is a named collection of Python types. A PushType
can be used to determine if multiple items should be considered the same type
during Push program execution.

"""
from typing import List, Sequence, Tuple

import numpy as np
from pyrsistent import CheckedPVector

from pyshgp.validation import PushError


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
        super().__init__()
        if len(char) == 0:
            raise PushError.empty_character()
        if len(char) > 1:
            raise PushError.long_character()

    def __eq__(self, other):
        return isinstance(other, Char) and str(self) == str(other)


class PushType:
    """Type information for values used by Push programs.

    Attributes
    ----------
    name : str
        A name for the type. Used when referencing the PushType in Instruction
        definitions and will be the key in the PushState for the corresponding
        PushStack.
    is_collection : bool, optional
        Indicates if that the PushType is a collection. Default is False.
    is_numeric : bool, optional
        Indicates if that the PushType is a numeric type. Default is False.

    """

    def __init__(self,
                 name: str,
                 python_types: Tuple[type, ...],
                 is_collection: bool = False,
                 is_numeric: bool = False):
        self.name = name
        self.python_types = python_types
        self.is_collection = is_collection
        self.is_numeric = is_numeric

    def is_instance(self, value) -> bool:
        return isinstance(value, self.python_types)

    def coerce(self, value):
        return self.python_types[0](value)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and self.name == other.name

    def __hash__(self):
        return (str(self.__class__) + self.name).__hash__()


class PushBoolType(PushType):

    def __init__(self):
        super().__init__("bool", (bool, np.bool_))


class PushIntType(PushType):

    def __init__(self):
        super().__init__("int", (int, np.int64, np.int32, np.int16, np.int8), is_numeric=True)


class PushFloatType(PushType):

    def __init__(self):
        super().__init__("float", (float, np.float64, np.float32, np.float16), is_numeric=True)


class PushCharType(PushType):

    def __init__(self):
        super().__init__("char", (Char,))


class PushStrType(PushType):

    def __init__(self):
        super().__init__("str", (str, np.str_, np.object_))


class PushVectorType(PushType):

    def __init__(self, name: str, p_vec_type):
        super().__init__(name, (p_vec_type,), is_collection=True)
        self.p_vec_type = p_vec_type

    def coerce(self, value):
        el_type = self.p_vec_type.__type__
        return self.p_vec_type([el_type(el) for el in value])


class BoolVector(CheckedPVector):
    __type__ = bool


class IntVector(CheckedPVector):
    __type__ = int


class FloatVector(CheckedPVector):
    __type__ = float


class CharVector(CheckedPVector):
    __type__ = Char


class StrVector(CheckedPVector):
    __type__ = str


_py2vec = {
    bool: BoolVector,
    int: IntVector,
    float: FloatVector,
    Char: CharVector,
    str: StrVector,
}


def make_vector_type(scalar_type: PushType):
    return PushVectorType("vector_" + scalar_type.name, _py2vec[scalar_type.python_types[0]])


PushInt = PushIntType()
PushFloat = PushFloatType()
PushStr = PushStrType()
PushBool = PushBoolType()
PushChar = PushCharType()

PushIntVector = make_vector_type(PushInt)
PushFloatVector = make_vector_type(PushFloat)
PushStrVector = make_vector_type(PushStr)
PushBoolVector = make_vector_type(PushBool)
PushCharVector = make_vector_type(PushChar)


CORE_SCALAR_PUSH_TYPES: List[PushType] = [
    PushBool,
    PushInt,
    PushChar,
    PushFloat,
    PushStr,
]


CORE_VECTOR_PUSH_TYPES: List[PushVectorType] = [
    PushIntVector,
    PushFloatVector,
    PushStrVector,
    PushBoolVector,
    PushCharVector,
]


CORE_PUSH_TYPES: List[PushType] = CORE_SCALAR_PUSH_TYPES + CORE_VECTOR_PUSH_TYPES
