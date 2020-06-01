"""The state module is define the PushState class.

A PushState object holds the PushStacks, stdout string, and collection of input
values. The PushState is what controls the setup of all stacks before program
manipulation, and the producing of outputs after program execution.
"""
from typing import Sequence, Union
from collections import deque
import numpy as np
from pyshgp.push.config import PushConfig

from pyshgp.push.type_library import PushTypeLibrary
from pyshgp.push.atoms import CodeBlock
from pyshgp.push.stack import PushStack
from pyshgp.utils import Token


class PushState(dict):
    """A collection of PushStacks used during push program execution."""

    __slots__ = ["stdout", "inputs", "untyped", "type_library", "push_config"]

    def __init__(self, type_library: PushTypeLibrary, push_config: PushConfig):
        super().__init__()
        self.stdout = ""
        self.inputs = []
        self.untyped = deque([])
        self.type_library = type_library
        self.push_config = push_config

        for name, push_type in type_library.items():
            self[name] = PushStack(push_type, push_config)

    def __eq__(self, other) -> bool:
        if not isinstance(other, PushState):
            return False
        return super().__eq__(other) and self.inputs == other.inputs and self.stdout == other.stdout

    @classmethod
    def from_dict(cls, d, type_library: PushTypeLibrary, push_config: PushConfig):
        """Set the state to match the given dictionary.

        .. warning::
            This is written to be used in ``pyshgp`` tests, NOT as part of
            push program execution or evolution. There are no checks to confirm
            that the ``d`` can be converted to a valid Push state.

        Parameters
        ----------
        d : dict
            Dict that is converted into a Push state.
        type_library : PushTypeLibrary
            A Push type library.

        """
        state = cls(type_library, push_config)
        inputs = []
        stdout = ""
        for k, v in d.items():
            if k == 'inputs':
                inputs = v
            elif k == 'stdout':
                stdout += v
            elif k == "untyped":
                for el in v:
                    state.untyped.append(el)
            else:
                for el in v:
                    state[k].push(el)
        state.load_inputs(inputs)
        state.stdout = stdout
        return state

    def load_code(self, program: CodeBlock):
        """Push the given CodeBlock to the execution stack."""
        self["exec"].push(program)

    def load_inputs(self, inputs):
        """Load a list of input values onto the PushState inputs.

        Parameters
        ----------
        inputs : list
            List of input values.

        """
        if not isinstance(inputs, (list, np.ndarray)):
            raise ValueError(
                "Push inputs must be a list, got {t}".format(t=type(inputs)))
        self.inputs = inputs

    def observe_stacks(self, types: Sequence[str]) -> list:
        """Return a list of output values based on the given types indicated.

        Items are take from the tops of each stack. If multiple occurences of
        the same type are in ``output_types``, the returned values are taken
        from progressively deeper in that stack. Does not pop the values off
        the stacks.

        Parameters
        ----------
        types : list
            List of strings denoting the push types of the returned values.

        """
        values = []
        counts = {}
        for typ in types:
            if typ == "stdout":
                values.append(self.stdout)
            else:
                ndx = counts.get(typ, 0)
                values.append(self[typ].nth(ndx))
                counts[typ] = ndx + 1
        return values

    def pop_from_stacks(self, types: Sequence[str]) -> Union[Sequence, Token]:
        """Pop the top items for each value_type. Return a vector of the values popped from each stack."""
        values = []
        for typ in types:
            val = self[typ].top()
            if val is Token.no_stack_item:
                return Token.revert
            else:
                values.append(val)
                self[typ].pop()
        return values

    def push_to_stacks(self, values: list, types: Sequence[str]):
        """Check that all values can be coerced into their expected PushType. Push them onto the correct stack."""
        for ndx in range(len(values)):
            val = values[ndx]
            typ = types[ndx]
            if typ == "stdout":
                self.stdout += str(val)
            elif typ == "untyped":
                self.untyped.append(val)
            else:
                self[typ].push(val)

    def size(self):
        """Return the size of the PushState."""
        return sum([len(s) for s in self.values()]) + len(self.inputs)

    def pretty_print(self):
        """Print the state of all stacks in the PushState."""
        for k, v in self.items():
            print(" ".join([k, ":", str(v)]))
        print("untyped : " + str(self.untyped))
        print("inputs : " + str(self.inputs))
        print("stdout : " + str(self.stdout))
