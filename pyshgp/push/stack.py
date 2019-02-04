# -*- coding: utf-8 -*-
"""The :mod:`stack` module defines the ``PushStack`` class.

A PushStack is used to hold values of a certain PushType in a PushState object.
"""
from typing import Optional

from pyshgp.push.types import PushType
from pyshgp.utils import Token


class PushStack(list):
    """Stack that holds elements of a sinlge PushType.

    Parameters
    ----------
    push_type : PushType
        The PushType all items of the stack should conform to, or be coerced into.

    Attributes
    ----------
    push_type : PushType
        The PushType all items of the stack should conform to, or be coerced into.

    """

    __slots__ = ["push_type"]

    def __init__(self, push_type: PushType):
        self.push_type = push_type

    def is_empty(self) -> bool:
        """Return True if the stack is empty. Return False otherwise."""
        return len(self) == 0

    def push(self, value):
        """Pushes a value to the top of the stack.

        An alias for `append` which makes the definition of push instructions
        more clear.

        Parameters
        ----------
        value :
            Value to push onto stack.

        """
        if not self.push_type.is_instance(value):
            value = self.push_type.coerce(value)
        self.append(value)
        return self

    def pop(self, index: Optional[int] = None):
        """Pop the top item off the stack.

        Parameters
        ----------
        index :
            Index to pop from the stack.

        Returns
        --------
        Element at ``index`` in stack.

        """
        if index is None:
            return super().pop()
        else:
            return super().pop((len(self) - 1) - index)

    def nth(self, position: int):
        """Return the element at a given position.

        If stack is empty, returns None. If ``position < 0`` or
        ``position > len(self)`` returns a ``no_stack_item`` token.

        Parameters
        ----------
        position : int
            Position in stack to get item.

        Returns
        --------
        Element at ``positon`` in stack.

        """
        if len(self) <= position:
            return Token.no_stack_item
        elif len(self) == 0:
            return Token.no_stack_item
        else:
            return self[(len(self) - 1) - position]

    def take(self, n: int):
        """Return the top `n` items from the tack.

        If `n` is less than zero, result is an empty list. If `n` is greater
        than the size of the stack, result contains every element.

        Parameters
        ----------
        n : int
            Number of items

        Returns
        --------
        Element at ``positon`` in stack.

        """
        if n < 0:
            return []
        return self[:-(n + 1):-1]

    def top(self):
        """Return the top item on the stack, or a ``no_stack_item`` token if empty.

        Returns
        --------
        Returns the top element of the stack, or None if empty.

        """
        if len(self) > 0:
            return self[-1]
        else:
            return Token.no_stack_item

    def insert(self, position: int, value):
        """Insert value at position in stack.

        Parameters
        ----------
        position : int
            Position in stack to get item.
        value :
            Value to insert into stack.

        """
        if not self.push_type.is_instance(value):
            value = self.push_type.coerce(value)
        super().insert(len(self) - position, value)
        return self

    def set_nth(self, position: int, value):
        """Overwrite the item in the nth position of the stack with the new value.

        Parameters
        ----------
        position : int
            Position in stack to get item.
        value :
            Value to insert into stack.

        """
        if not self.push_type.is_instance(value):
            value = self.push_type.coerce(value)
        self[len(self) - 1 - position] = value
        return self

    def flush(self):
        """Empty the stack."""
        del self[:]
        return self

    def __repr__(self):
        self_r = list(self)[::-1]
        return self_r.__repr__()

    def __eq__(self, other):
        if not isinstance(other, PushStack):
            return False
        return self.push_type == other.push_type and list(self) == list(other)
