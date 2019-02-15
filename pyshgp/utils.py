"""Utility classes and functions used throughout pyshgp."""
from typing import Optional, Union
from abc import ABC, abstractmethod
from enum import Enum

import numpy as np
from numpy.random import choice


class DiscreteProbDistrib:
    """Discrete Probability Distribution."""

    __slots__ = ["elements", "_total", "_raw_probabilities", "_normalized_probabilities"]

    def __init__(self):
        self.elements = []
        self._total = 0.0
        self._raw_probabilities = []
        self._normalize()

    def _normalize(self):
        self._normalized_probabilities = np.array(self._raw_probabilities) / self._total

    def add(self, el, p):
        """Add an element with a relative probability."""
        self.elements.append(el)
        self._total += float(p)
        self._raw_probabilities.append(p)
        self._normalize()
        return self

    def size(self):
        """Return the number of elements in the distribution."""
        return len(self.elements)

    def sample(self):
        """Return a sample from the distribution."""
        if self.size() == 1:
            return self.elements[0]
        return choice(self.elements, p=self._normalized_probabilities)

    def sample_n(self, n: int = 1, replace: bool = True):
        """Return n samples from the distribution."""
        if self.size() == 1 and replace:
            return [self.elements[0]] * n
        return choice(self.elements, n, replace, self._normalized_probabilities)


class Token(Enum):
    """Enum class of all Tokens."""

    no_stack_item = 1
    revert = 2
    whole_state = 3


class PushError(Exception):
    """Error raised during Push program execution."""

    @classmethod
    def no_type(cls, thing):
        """Raise PushError when no PushType can be found for something."""
        return cls("Unkown PushType for {th}.".format(th=thing))

    @classmethod
    def failed_coerce(cls, thing, push_type):
        """Raise PushError when something fails to coerce to a PushType."""
        return cls("Could not convert {typ1} {th} to {typ2}.".format(
            th=thing,
            typ1=type(thing),
            typ2=push_type
        ))

    @classmethod
    def empty_character(cls):
        """Raise PushError when Character is made from empty string."""
        return cls("Character object cannot be created from empty string.")

    @classmethod
    def long_character(cls):
        """Raise PushError when Character is made from string length more than 1."""
        return cls("Character object cannot be created from string of length > 1.")


class JSONable(ABC):
    """Abstract base class for objects can be transformed into JSON."""

    @abstractmethod
    def jsonify(self) -> str:
        """Return the object as a JSON string."""
        pass

    def to_json(self, filepath: Optional[str] = None) -> Optional[str]:
        """Write the object to either a string or a file."""
        json_str = self.jsonify()
        if filepath is None:
            return json_str
        else:
            with open(filepath, "w+") as f:
                f.write(json_str)


def jsonify_collection(root: Union[list, dict]) -> str:
    """Return the given list or dict and all elements as a JSON string."""
    def _helper(thing) -> str:
        if isinstance(thing, list):
            return "[" + ",".join([_helper(el) for el in thing]) + "]"
        elif isinstance(thing, dict):
            return "{" + ",".join([str(k) + ":" + _helper(v) for k, v in thing.items()]) + "}"
        elif isinstance(thing, JSONable):
            return thing.jsonify()
        else:
            return str(thing)

    if isinstance(root, (list, dict)):
        return _helper(root)
    else:
        raise ValueError("Can jsonify_collection lists and dicts. Got {t}.".format(t=type(root)))
