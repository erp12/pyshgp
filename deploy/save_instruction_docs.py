import argparse
import os

import pyshgp

from pyshgp.push.instruction import (
    Instruction,
    SimpleInstruction,
    StateToStateInstruction,
    TakesStateInstruction,
    ProducesManyOfTypeInstruction,
)
from pyshgp.push.instructions import core_instructions
from pyshgp.push.type_library import PushTypeLibrary


CORE_INSTRUCTIONS = core_instructions(PushTypeLibrary())
DOC_DIR = "docs_source/source"


def _generate_instruction_rst(instr: Instruction) -> str:
    lines = [instr.name, "=" * len(instr.name)]

    signature_line = None
    signature_template = "*Takes: {i} - Produces: {o}*"
    if isinstance(instr, SimpleInstruction):
        signature_line = signature_line = signature_template.format(
            i="[" + ", ".join(instr.input_stacks) + "]",
            o="[" + ", ".join(instr.output_stacks) + "]"
        )
    elif isinstance(instr, StateToStateInstruction):
        signature_line = signature_template.format(i="PushState", o="PushState")
    elif isinstance(instr, TakesStateInstruction):
        signature_line = signature_template.format(
            i="PushState",
            o="[" + ", ".join(instr.output_stacks) + "]"
        )
    elif isinstance(instr, ProducesManyOfTypeInstruction):
        signature_line = signature_template.format(
            i="[" + ", ".join(instr.input_stacks) + "]",
            o="Arbitrary number of {t} values.".format(t=instr.output_stack)
        )

    if instr.code_blocks > 0:
        signature_line = signature_line[:-1] + " - Opens {c} code blocks*".format(c=instr.code_blocks)

    lines.append(signature_line + "\n")
    lines.append(instr.docstring)
    return "\n".join(lines)


if __name__ == "__main__":
    os.makedirs(DOC_DIR, exist_ok=True)
    ver = str(pyshgp.__version__)
    save_ver = "v" + ver.replace(".", "_")
    with open(os.path.join(DOC_DIR, save_ver + "_core_instructions.rst"), "w") as f:

        title = "PyshGP Core Instruction Set\n"

        f.write("*" * len(title) + "\n")
        f.write(title)
        f.write("*" * len(title) + "\n")

        for instr in CORE_INSTRUCTIONS:
            f.write("\n" + _generate_instruction_rst(instr) + "\n")
