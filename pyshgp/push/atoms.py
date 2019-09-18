"""The :mod:`atoms` module defines all types of Push Atoms.

An Atom is a peice of code in the Push language. A Literal Atom is a constant
value of one of the supported PushType. An Instruction Atom is a wrapped
function that can be used to manipulate a PushState. A CodeBlock is a sequence
of other Atoms is used to express nested expressions of code.
"""
from abc import ABC, abstractmethod
from collections import MutableSequence
from typing import Any, Sequence
from itertools import chain, count

from pyshgp.push.types import PushType
from pyshgp.utils import Saveable, Copyable


class Atom:
    """Base class of all Atoms. The fundamental element of Push programs."""

    ...


class Closer(Atom):
    """An Atom dedicated to denoting the close of a CodeBlock in its flat representsion."""

    def __eq__(self, other):
        return isinstance(other, Closer)

    def __repr__(self) -> str:
        return "CLOSER"


class Literal(Atom):
    """An Atom which holds a constant value.

    Parameters
    ----------
    value : Any
        The value to be stored in Literal.
    push_type : PushType, optional
        The PushType of the Literal. Usually, the PushType's underlying native
        type is the same as the type of the Literal's value. The PushType is
        used to determine how to route the Literal onto the correct PushStack
        of the PushState during program execution. If push_type is none, the
        PushType will attempt to be infered from the type of the value.

    """

    __slots__ = ["push_type", "value"]

    def __init__(self, value: Any, push_type: PushType):
        self.push_type = push_type
        if not self.push_type.is_instance(value):
            print("THIS?")
            value = self.push_type.coerce(value)
        self.value = value

    def __eq__(self, other):
        if isinstance(other, Literal) and self.push_type == other.push_type:
            return self.value == other.value
        return False

    def __repr__(self) -> str:
        return str(self.value)


class Instruction(Atom, ABC):
    """An Atom which holds a function used to modify the PushStateself.

    The Instruction class is the abstract base class for specific implemenations
    that are configured differently. For example, see SimpleInstruction verses
    TakesStateInstruction.

    Parameters
    ----------
    name : str,
        A unique name for the instruction.
    code_blocks : int
        The number of CodeBlocks to open following the instruction in a Genome.
    docstring : str, optional
        A string describing in the behavior of the Instruction.

    Attributes
    ----------
    name : str,
        A unique name for the instruction.
    code_blocks : int
        The number of CodeBlocks to open following the instruction in a Genome.
    docstring : str, optional
        A string describing in the behavior of the Instruction.

    """

    __slots__ = ["name", "code_block", "docstring"]

    def __init__(self, name: str, code_blocks: int, docstring="Write me!"):
        self.name = name
        self.code_blocks = code_blocks
        self.docstring = docstring

    @abstractmethod
    def evaluate(self, push_state, push_config=None):
        """Evaluate the instruction on the given PushState.

        Parameters
        ----------
        push_state: pyshgp.push.state.PushState
            The PushState to run the instruction on.
        push_config: pyshgp.push.interpreter.PushConfig
            The configuration of the Push language.

        Returns
        -------
        pyshgp.push.state.PushState
            Return the given state, possibly modified by the Instruction.

        """
        # Can't annotate types properly due to circular import.
        pass

    @abstractmethod
    def required_stacks(self) -> Sequence[str]:
        """Return a list of PushType names relevant to the instruction."""
        pass

    def __eq__(self, other):
        if type(self) == type(other):
            return self.name == other.name
        return False

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        return "Instruction<{n}>".format(n=self.name)


class JitInstructionRef(Atom):
    """Just-In-Time Instruction Reference.

    A JitInstructionRef is a placeholder atom. When a PushInterpreter evaluates
    a Just-In-Time Instruction Reference, it searches for an instruction with a
    specific name in its InstructionSet. If found, this instruction is
    evaluated by the PushInterpreter.

    A JitInstructionRef should be used when Instruction's function definition
    must refer to another instruction, including its own instruction.

    Parameters
    ----------
    name: str
        The name of the Instruction being referenced.

    """

    __slots__ = ["name"]

    def __init__(self, name: str):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, JitInstructionRef):
            return self.name == other.name
        return False

    def __repr__(self):
        return "JitInstructionRef<{n}>".format(n=self.name)


class CodeBlock(MutableSequence, Atom, Saveable, Copyable):
    """An Atom which holds a sequence of other Atoms."""

    def __init__(self, *args):
        self.list = []
        for el in args:
            self.append(el)

    def __getitem__(self, i: int) -> Any:
        return self.list.__getitem__(i)

    def __setitem__(self, i: int, o: Any) -> None:
        atom = CodeBlock._conform_element(o)
        self.__setitem__(i, atom)

    def __delitem__(self, i: int) -> None:
        self.list.__delitem__(i)

    def __len__(self) -> int:
        return self.list.__len__()

    def __eq__(self, other):
        return isinstance(other, CodeBlock) and self.list == other.list

    def __repr__(self):
        return "CodeBlock" + self.list.__repr__()

    def append(self, atom: Atom) -> None:
        """Append an Atom to the end of the CodeBlock."""
        self.list.append(CodeBlock._conform_element(atom))

    def insert(self, index: int, atom: Atom) -> None:
        """Insert Atom before index."""
        self.list.insert(index, CodeBlock._conform_element(atom))

    @staticmethod
    def _conform_element(el: Any) -> Atom:
        if isinstance(el, CodeBlock):
            return el.copy()
        elif isinstance(el, Atom):
            return el
        elif isinstance(el, list):
            return CodeBlock(*el)
        else:
            raise ValueError("Only Atoms can be added to CodeBlocks. Got {el}".format(el=el))

    def size(self, depth: int = 1) -> int:
        """Return the size of the block and the size of all the nested blocks."""
        return sum([el.size(depth + 1) + 1 if isinstance(el, CodeBlock) else 1 for el in self])

    def depth(self) -> int:
        """Return the farthest depth of the CodeBlock."""
        i = iter(self)
        try:
            for level in count():
                i = chain([next(i)], i)
                i = chain.from_iterable(s for s in i if isinstance(s, Sequence) and not isinstance(s, str))
        except StopIteration:
            return level
        return 0

    def code_at_point(self, ndx: int) -> Atom:
        """Return a nested element of the CodeBlock using depth first traversal."""
        if ndx == 0:
            return self
        i = ndx
        for el in self:
            i = i - 1
            if i == 0:
                return el
            if isinstance(el, CodeBlock):
                next_depth = el.code_at_point(i)
                if next_depth is not None:
                    return next_depth
                i = i - el.size()

    def insert_code_at_point(self, code: Atom, index: int):
        """Insert an element into the CodeBlock using depth first traversal."""
        i = index
        for ndx, el in enumerate(self):
            if i == 0:
                if isinstance(code, CodeBlock):
                    code = code.copy(True)
                self.insert(ndx, code)
                return self
            i = i - 1
            if isinstance(el, CodeBlock):
                next_depth = el.insert_code_at_point(code, i)
                if next_depth is not None:
                    return self
                i = i - el.size()
