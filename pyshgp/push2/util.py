from typing import *
from enum import Enum


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
        super(Char, self).__init__()
        if len(char) == 0:
            raise ValueError("Char object cannot be created from empty string.")
        if len(char) > 1:
            raise ValueError("Char object cannot be created from string of length > 1.")


class Token(Enum):
    """Enum class of all Tokens."""

    NO_ITEM = 1
    NOOP = 2
    WHOLE_STATE = 3


def constrain_collection(max_size: int, coll: Sequence) -> Sequence:
    """Constrains the collection to a size that is safe for Push program execution."""
    if len(coll) > max_size:
        return coll[:max_size]
    return coll


def constrain_number(max_magnitude: float, n: Union[int, float]) -> Union[int, float]:
    """Constrains the number to a magnitude that is safe for Push program execution."""
    if abs(n) > max_magnitude:
        sign = -1 if n < 0 else 1
        return max_magnitude * sign
    # Return the same the numeric type as given
    return type(n)(n)
