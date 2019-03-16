"""The :mod:`atoms` module defines all types of Push Atoms.

An Atom is a peice of code in the Push language. A Literal Atom is a constant
value of one of the supported PushType. An Instruction Atom is a wrapped
function that can be used to manipulate a PushState. A CodeBlock is a sequence
of other Atoms is used to express nested expressions of code.
"""
from abc import ABC, abstractmethod
from typing import Any, Sequence
from itertools import chain, count
import json
from copy import copy, deepcopy

from pyshgp.push.types import PushType, push_type_by_name, push_type_of
from pyshgp.utils import JSONable, jsonify_collection


class Atom(JSONable):
    """Base class of all Atoms. The fundamental element of Push programs."""

    @classmethod
    def is_instance(cls, thing: Any) -> bool:
        """Return True if thing is Atom or subclass. Otherwise return False.

        Needed for when used as JIT PushType.

        Parameters
        ----------
        thing
            Anything.

        Returns
        -------
        bools
            Returns True if thing is an Atom or subclass of Atom. Returns False otherwise.

        """
        return isinstance(thing, cls)

    @classmethod
    def coerce(cls, thing: Any):
        """Convert thing into Atom by wrapping in Literal."""
        return Literal(thing)


class Closer(Atom):
    """An Atom dedicated to denoting the close of a CodeBlock in its flat representsion."""

    def jsonify(self) -> str:
        """Return the object as a JSON string."""
        return json.dumps({"a": "close"}, separators=(',', ':'))

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

    def __init__(self, value: Any, push_type: PushType = None):
        self.push_type = push_type_of(value) if push_type is None else push_type
        if not self.push_type.is_instance(value):
            value = self.push_type.coerce(value)
        self.value = value

    def jsonify(self) -> str:
        """Return the object as a JSON string."""
        return json.dumps(
            {"a": "lit", "t": self.push_type.name, "v": self.value},
            separators=(',', ':')
        )

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
    def evaluate(self, push_state, interpreter_config=None):
        """Evaluate the instruction on the given PushState.

        Parameters
        ----------
        push_state: pyshgp.push.state.PushState
            The PushState to run the instrution on.
        interpreter_config: pyshgp.push.interpreter.PushInterpreterConfig
            The configuration of the Interpreter.

        Returns
        -------
        pyshgp.push.state.PushState
            Return the given state, possibly modified by the Instruction.

        """
        # Can't annotate types properly due to circular import.
        pass

    @abstractmethod
    def relevant_types(self) -> Sequence[str]:
        """Return a list of PushType names relevant to the instruction."""
        pass

    def jsonify(self) -> str:
        """Return the object as a JSON string."""
        return json.dumps({"a": "instr", "n": self.name}, separators=(',', ':'))

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

    def jsonify(self) -> str:
        """Return the object as a JSON string."""
        return json.dumps({"a": "jit-instr", "n": self.name}, separators=(',', ':'))

    def __eq__(self, other):
        if isinstance(other, JitInstructionRef):
            return self.name == other.name
        return False

    def __repr__(self):
        return "JitInstructionRef<{n}>".format(n=self.name)


class CodeBlock(list, Atom):
    """An Atom which holds a sequence of other Atoms."""

    def __init__(self, *args):
        for el in args:
            self._add(el)

    def _add(self, el):
        if isinstance(el, CodeBlock):
            self.append(el.copy())
        elif isinstance(el, Atom):
            self.append(el)
        elif isinstance(el, list):
            self.append(CodeBlock.from_list(el))
        else:
            raise ValueError("Only Atoms can be added to CodeBlocks. Got {el}".format(el=el))

    @staticmethod
    def from_list(l: Sequence[Atom]):
        """Return a CodeBlock from a list of Atoms."""
        cb = CodeBlock()
        for el in l:
            cb._add(el)
        return cb

    @staticmethod
    def from_json_str(json_str: str, instruction_set: dict):
        """Create a CodeBlock from a JSON string."""
        # Can't annotate instruction_set type properly due to circular import.
        return AtomFactory.json_list_to_code_block(json.loads(json_str), instruction_set)

    def jsonify(self) -> str:
        """Return the object as a JSON string."""
        return jsonify_collection(self)

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

    def copy(self, deep: bool = False):
        """Copy the CodeBlock."""
        return deepcopy(self) if deep else copy(self)


class AtomFactory:
    """Produces specific types of Atoms from various sources.

    Any kinds of Atoms except CodeBlocks can be described in a dict. CodeBlocks
    can be described as lists of other Atom specifications. These representations
    are used for serialization and deserialization (JSON). The AtomFactory builds
    Atoms of any kind from these specifications.
    """

    # Can't annotate instruction_set type properly due to circular import.
    @staticmethod
    def json_dict_to_atom(json_dict: dict, instruction_set: dict) -> Atom:
        """Return the atom specified by the dict produced by JSON decoding."""
        atom_type = json_dict["a"]
        if atom_type == "close":
            return Closer()
        elif atom_type == "lit":
            push_type = push_type_by_name(json_dict["t"])
            value = push_type.coerce(json_dict["v"])
            return Literal(value, push_type)
        elif atom_type == "instr":
            return instruction_set[json_dict["n"]]
        elif atom_type == "jit-instr":
            return JitInstructionRef(json_dict["n"])
        else:
            raise ValueError("bad atom spec {s}".format(s=json_dict))

    # Can't annotate instruction_set type properly due to circular import.
    @staticmethod
    def json_list_to_code_block(json_list: list, instruction_set: dict) -> CodeBlock:
        """Return a CobdeBlock build from the list produced by JSON decoding."""
        cb = CodeBlock()
        for nested_atom_spec in json_list:
            if isinstance(nested_atom_spec, list):
                cb.append(AtomFactory.json_list_to_code_block(nested_atom_spec, instruction_set))
            else:
                cb.append(AtomFactory.json_dict_to_atom(nested_atom_spec, instruction_set))
        return cb

    # Can't annotate instruction_set type properly due to circular import.
    @staticmethod
    def json_str_to_atom_list(json_str: str, instruction_set: dict) -> Sequence[Atom]:
        """Return a list of Atoms parsed from the json_str."""
        atoms = []
        for atom_spec in json.loads(json_str):
            if isinstance(atom_spec, list):
                atoms.append(AtomFactory.json_list_to_code_block(atom_spec, instruction_set))
            else:
                atoms.append(AtomFactory.json_dict_to_atom(atom_spec, instruction_set))
        return atoms
