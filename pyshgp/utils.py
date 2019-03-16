"""Utility classes and functions used throughout pyshgp."""
from typing import Optional, Union
from abc import ABC, abstractmethod
from enum import Enum
import inspect

import numpy as np
from numpy.random import choice


def instantiate_using(cls: type, args: dict):
    """Call the given function using only the relevant kwargs present in the args dict."""
    arg_names = inspect.getfullargspec(cls)[0][1:]
    kwargs = {}
    for arg_name in arg_names:
        if arg_name in args:
            kwargs[arg_name] = args[arg_name]
    return cls(**kwargs)


def list_rindex(lst, el):
    """Index of the last occurrence of an item in a list. Return None is item not found."""
    for i in reversed(range(len(lst))):
        if lst[i] == el:
            return i
    return None


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


class Verbosity(Enum):
    """Enum class of all verbosity levels."""

    off = 1
    debug = 2
    on = 3


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
