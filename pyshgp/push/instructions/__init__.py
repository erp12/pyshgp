"""pyshgp.push.instructions."""
from typing import Sequence, Set, List
from itertools import chain

from pyshgp.push.type_library import PushTypeLibrary
from pyshgp.push.instruction import Instruction
from pyshgp.push.instructions import common, numeric, text, code, io, logical, vector


def _supported(instructions: Sequence[Instruction], supported_stacks: Set[str]) -> Sequence[Instruction]:
    supported = []
    for instr in instructions:
        if instr.required_stacks() <= supported_stacks:
            supported.append(instr)
    return supported


def generic_instructions(type_library: PushTypeLibrary) -> List[Instruction]:
    """All instructions that can be applied to any stack, regardless of PushType."""
    return list(chain(
        io.instructions(type_library),
        common.instructions(type_library),
    ))


def core_instructions(type_library: PushTypeLibrary) -> Sequence[Instruction]:
    """All instructions defined by pyshgp for the given type library."""
    supported_stacks = type_library.supported_stacks()
    instruction_modules = [numeric, text, logical, code, vector]
    basic_instr = list(chain(*[m.instructions(type_library) for m in instruction_modules]))
    gen_instrs = generic_instructions(type_library)
    supported_instructions = _supported(basic_instr + gen_instrs, supported_stacks)
    return supported_instructions
