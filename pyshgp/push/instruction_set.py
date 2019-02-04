"""The :mod:`instruction_set` module defines the InstructionSet class.

An InstructionSet is a collection of Instruction objects, stored by name. The
InstructionSet has methods to help define and register additional instructions.
"""
from typing import Sequence, Set
from itertools import chain
import re

from pyshgp.push.atoms import Instruction
from pyshgp.push.types import PushType
from pyshgp.push.instructions import common, numeric, text, code, io, logical


_CORE_INSTRUCTIONS = list(chain(
    common.instructions(),
    code.instructions(),
    numeric.instructions(),
    text.instructions(),
    io.instructions(),
    logical.instructions(),
))


class InstructionSet(dict):
    """A collection of Instruction objects stored by name.

    Parameters
    ----------
    register_all : bool, optional
        If True, all instructions in the core instruction set will be registered
        upon instanciation. Default is False.
    strip_docstrings : bool, optional
        If True, the docstring attribute of registered instructions will be
        removed to reduce memory footprint. Default is True.

    Attributes
    ----------
    register_all : bool, optional
        If True, all instructions in the core instruction set will be registered
        upon instanciation. Default is False.
    strip_docstrings : bool, optional
        If True, the docstring attribute of registered instructions will be
        removed to reduce memory footprint. Default is True.

    """

    def __init__(self, *, register_all: bool = False, strip_docstrings: bool = True):
        self.strip_docstrings = strip_docstrings
        if register_all:
            self.register_all()

    def register(self, instr: Instruction):
        """Register an Instruction object.

        Parameters
        ----------
        instr
            Instruction to register.

        Returns
        -------
        InstructionSet
            A reference to the InstructionSet.

        """
        if self.strip_docstrings and hasattr(instr, "docstring"):
            del instr.docstring
        self[instr.name] = instr
        return self

    def register_list(self, instrs: Sequence[Instruction]):
        """Register a list of Instruction ojbects.

        Parameters
        ----------
        instrs
            List of Instruction objects to register.

        Returns
        -------
        InstructionSet
            A reference to the InstructionSet.

        """
        for i in instrs:
            self.register(i)
        return self

    def register_by_type(self, type_names: Sequence[str], *, exclude: Sequence[str] = None):
        """Register all instructions that make use of the given type name.

        Parameters
        ----------
        type_names
            List of PushType names.

        Returns
        -------
        InstructionSet
            A reference to the InstructionSet.

        """
        for i in _CORE_INSTRUCTIONS:
            for type_name in type_names:
                i_types = i.relevant_types()
                if type_name in i_types:
                    include = True
                    if exclude is not None:
                        for i_type in i_types:
                            if i_type in exclude:
                                include = False
                    if include:
                        self.register(i)
                    break
        return self

    def register_by_name(self, name_pattern: str):
        """Register all instructions whose name match the given pattern.

        Parameters
        ----------
        name_pattern
            A regex string.

        Returns
        -------
        InstructionSet
            A reference to the InstructionSet.

        """
        re_pat = re.compile(name_pattern)
        for i in _CORE_INSTRUCTIONS:
            if re.match(re_pat, i.name) is not None:
                self.register(i)
        return self

    def register_all(self):
        """Register all core instructions defined in pyshgp.

        Returns
        -------
        InstructionSet
            A reference to the InstructionSet.

        """
        self.register_list(_CORE_INSTRUCTIONS)
        return self

    def register_n_inputs(self, n: int):
        """Create and register `n` input instructions.

        Parameters
        ----------
        n
            The number of input instructions to make.

        Returns
        -------
        InstructionSet
            A reference to the InstructionSet.

        """
        input_instructions = io.make_input_instructions(n)
        self.register_list(input_instructions)
        return self

    def unregister(self, instruction_name: str):
        """Unregister an instruction by name.

        Parameters
        ----------
        instruction_name
            The name of the instruciton to unregister.

        Returns
        -------
        InstructionSet
            A reference to the InstructionSet.

        """
        self.pop(instruction_name, None)
        return self

    def supported_types(self) -> Set[PushType]:
        """Return all PushTypes used through the registered instructions.

        Returns
        -------
        Set[PushType]
            The set of PushTypes that are used by the registered instructions.

        """
        all_types = set()
        for instr in self.values():
            all_types.update(instr.relevant_types())
        return all_types
