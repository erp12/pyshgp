"""The :mod:`instruction_set` module defines the InstructionSet class.

An InstructionSet is a collection of Instruction objects, stored by name. The
InstructionSet has methods to help define and register additional instructions.
"""
from typing import Sequence, Set
import re

from pyshgp.push.type_library import PushTypeLibrary, RESERVED_PSEUDO_STACKS
from pyshgp.push.atoms import Instruction
from pyshgp.push.instructions import core_instructions, io


class InstructionSet(dict):
    """A collection of Instruction objects stored by name.

    Parameters
    ----------
    type_library : PushTypeLibrary, optional
        The PushTypeLibrary which denote the PushTypes (and thus stacks)
        are supported. Default is None, which corresponds to the core set of types.
    register_all : bool, optional
        If True, all instructions in the core instruction set will be registered
        upon instanciation. Default is False.
    strip_docstrings : bool, optional
        If True, the docstring attribute of registered instructions will be
        removed to reduce memory footprint. Default is True.

    Attributes
    ----------
    type_library : PushTypeLibrary, optional
        The PushTypeLibrary which denote the PushTypes (and thus stacks)
        are supported. Default is None, which corresponds to the core set of types.
    register_all : bool, optional
        If True, all instructions in the core instruction set will be registered
        upon instanciation. Default is False.
    strip_docstrings : bool, optional
        If True, the docstring attribute of registered instructions will be
        removed to reduce memory footprint. Default is True.

    """

    def __init__(self, type_library: PushTypeLibrary = None, register_core: bool = False, strip_docstrings: bool = True):
        self.strip_docstrings = strip_docstrings

        if type_library is None:
            type_library = PushTypeLibrary()
        self.type_library = type_library

        if register_core:
            self.register_core()

    def set_type_library(self, type_library: PushTypeLibrary):
        """Set the type library attribute and return self.

        Parameters
        ----------
        type_library
            PushTypeLibrary to set.

        Returns
        -------
        InstructionSet
            A reference to the InstructionSet.

        """
        self.type_library = type_library
        return self

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
        if instr.required_stacks() <= self.type_library.supported_stacks():
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

    def register_core_by_stack(
        self,
        include_stacks: Set[str],
        *,
        exclude_stacks: Set[str] = None
    ):
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
        for i in core_instructions(self.type_library):
            req_stacks = i.required_stacks()
            if req_stacks <= include_stacks:
                if exclude_stacks is not None and len(req_stacks & exclude_stacks) > 0:
                    break
                self.register(i)
        return self

    def register_core_by_name(self, name_pattern: str):
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
        for i in core_instructions(self.type_library):
            if re.match(re_pat, i.name) is not None:
                self.register(i)
        return self

    def register_core(self):
        """Register all core instructions defined in pyshgp.

        Returns
        -------
        InstructionSet
            A reference to the InstructionSet.

        """
        self.register_list(core_instructions(self.type_library))
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

    def required_stacks(self) -> Set[str]:
        """Return all stack names used throughout the registered instructions.

        Returns
        -------
        Set[str]
            The set of stack names that are used by the registered instructions.

        """
        all_types = set()
        for instr in self.values():
            all_types.update(instr.required_stacks())
        return all_types - RESERVED_PSEUDO_STACKS
