"""Utility classes and functions used throughout pyshgp."""
from copy import deepcopy, copy
from enum import Enum
import inspect
import pickle
import os

import numpy as np


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
        return np.random.choice(self.elements, p=self._normalized_probabilities)

    def sample_n(self, n: int = 1, replace: bool = True):
        """Return n samples from the distribution."""
        if self.size() == 1 and replace:
            return [self.elements[0]] * n
        return np.random.choice(self.elements, n, replace, self._normalized_probabilities)


class Token(Enum):
    """Enum class of all Tokens."""

    no_stack_item = 1
    revert = 2
    whole_state = 3


class Saveable:
    """Allows a pickle-able class to be written and loaded from a file."""

    def save(self, path: str):
        """Save the CodeBlock to a binary file."""
        loc, filename = os.path.split(path)
        if loc != "":
            os.makedirs(loc, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(path: str):
        """Load a CodeBlock from a binary file.."""
        with open(path, "rb") as f:
            return pickle.load(f)


class Copyable:
    """Allows an object to be copied via a method."""

    def copy(self, deep: bool = False):
        """Copy the CodeBlock."""
        return deepcopy(self) if deep else copy(self)
