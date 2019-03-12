"""The state module is define the PushState class.

A PushState object holds the PushStacks, stdout string, and collection of input
values. The PushState is what controls the setup of all stacks before program
manipulation, and the producing of outputs after program execution.
"""
from typing import Sequence, Union, Set
import numpy as np

from pyshgp.push.types import PushType, push_type_by_name
from pyshgp.push.atoms import Atom, CodeBlock
from pyshgp.push.stack import PushStack
from pyshgp.utils import Token


class PushState(dict):
    """A collection of PushStacks used during push program execution."""

    __slots__ = ["stdout", "inputs", "_jit_push_types"]

    def __init__(self, push_types: Set[Union[PushType, str]]):
        super().__init__()
        self.stdout = ""
        self.inputs = []
        self._jit_push_types = {}

        for push_type in set(list(push_types) + ["exec"]):
            if isinstance(push_type, str):
                push_type_from_name = push_type_by_name(push_type)
                if push_type_from_name is None:
                    push_type = PushType(push_type, (Atom,))
                    push_type.coerce = Atom.coerce
                    self._jit_push_types[push_type.name] = push_type
                else:
                    push_type = push_type_from_name
            self._register_stack_of_type(push_type)

    def __eq__(self, other) -> bool:
        if not isinstance(other, PushState):
            return False
        return super().__eq__(other) and self.inputs == other.inputs and self.stdout == other.stdout

    def _register_stack_of_type(self, push_type: PushType):
        """Add a new stack."""
        self[push_type.name] = PushStack(push_type)

    @classmethod
    def from_dict(cls, d):
        """Set the state to match the given dictionary.

        .. warning::
            This is written to be used in ``pyshgp`` tests, NOT as part of
            push program execution or evolution. There are no checks to confirm
            that the ``d`` can be converted to a valid Push state.

        Parameters
        ----------
        d : dict
            Dict that is converted into a Push state.

        """
        state = cls(d.keys())
        inputs = []
        stdout = ""
        for k in d.keys():
            if k == 'inputs':
                inputs = d[k]
            elif k == 'stdout':
                stdout += d[k]
            else:
                for v in d[k]:
                    state[k].push(v)

        state.load_inputs(inputs)
        state.stdout = stdout
        return state

    def load_program(self, program: CodeBlock):
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
            else:
                self[typ].push(val)

    def size(self):
        """Return the size of the PushState."""
        return sum([len(s) for s in self.values()]) + len(self.inputs)

    def pretty_print(self, print_or_log_func=print):
        """Print the state of all stacks in the PushState."""
        for k, v in self.items():
            print_or_log_func(" ".join([k, ":", str(v)]))
        print_or_log_func(" ".join(['inputs :', str(self.inputs)]))
        print_or_log_func(" ".join(['stdout :', str(self.stdout)]))
