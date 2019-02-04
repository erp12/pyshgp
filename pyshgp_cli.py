"""PyshGP is intended to be used primarily as a library.

This main `pyshgp` module is intended to provide supporting features for user
and contributors.

Some of the features provided by this `pyshgp` module are:

- Generating documentation of the core supported instructions.

"""
import argparse
import os

import pyshgp

from pyshgp.push.atoms import Instruction
from pyshgp.push.instruction import (
    SimpleInstruction,
    StateToStateInstruction,
    TakesStateInstruction,
    ProducesManyOfTypeInstruction,
)
from pyshgp.push.instruction_set import _CORE_INSTRUCTIONS


DOC_DIR = "build/doc/"


def _generate_instruction_markdown(instr: Instruction) -> str:
    lines = []
    lines.append("### {n}".format(n=instr.name))

    signature_template = "_Takes: {i} - Produces: {o}_"
    if isinstance(instr, SimpleInstruction):
        signature_line = signature_line = signature_template.format(
            i="[" + ", ".join(instr.input_types) + "]",
            o="[" + ", ".join(instr.output_types) + "]"
        )
    elif isinstance(instr, StateToStateInstruction):
        signature_line = signature_template.format(i="PushState", o="PushState")
    elif isinstance(instr, TakesStateInstruction):
        signature_line = signature_template.format(
            i="PushState",
            o="[" + ", ".join(instr.output_types) + "]"
        )
    elif isinstance(instr, ProducesManyOfTypeInstruction):
        signature_line = signature_template.format(
            i="[" + ", ".join(instr.input_types) + "]",
            o="Arbitrary number of {t} values.".format(t=instr.output_type)
        )

    if instr.code_blocks > 0:
        signature_line = signature_line[:-1] + " - Opens {c} code blocks_".format(c=instr.code_blocks)

    lines.append(signature_line)
    lines.append(instr.docstring)
    return "\n".join(lines)


def _generate_instruction_html(instr: Instruction) -> str:
    lines = ["<li>"]
    lines.append('<h3 class="instr-name">{n}</h3>'.format(n=instr.name))

    signature_template = "Takes: {i} - Produces: {o}"
    if isinstance(instr, SimpleInstruction):
        signature_line = signature_line = signature_template.format(
            i="[" + ", ".join(instr.input_types) + "]",
            o="[" + ", ".join(instr.output_types) + "]"
        )
    elif isinstance(instr, StateToStateInstruction):
        signature_line = signature_template.format(i="PushState", o="PushState")
    elif isinstance(instr, TakesStateInstruction):
        signature_line = signature_template.format(
            i="PushState",
            o="[" + ", ".join(instr.output_types) + "]"
        )
    elif isinstance(instr, ProducesManyOfTypeInstruction):
        signature_line = signature_template.format(
            i="[" + ", ".join(instr.input_types) + "]",
            o="Arbitrary number of {t} values.".format(t=instr.output_type)
        )

    if instr.code_blocks > 0:
        signature_line = signature_line[:-1] + " - Opens {c} code blocks".format(c=instr.code_blocks)

    lines.append('<p class="instr-signature">{sl}</p>'.format(sl=signature_line))
    lines.append('<p class="instr-docstring">{ds}</p>'.format(ds=instr.docstring))
    lines.append("</li>")
    return "\n".join(lines)


def _generate_instruction_set_documentation(frmt: str):
    os.makedirs(DOC_DIR, exist_ok=True)
    with open(os.path.join(DOC_DIR, "instruction_set." + frmt), "w") as f:

        title = "PyshGP v{v} Instruction Set\n".format(v=pyshgp.__version__)

        if frmt == "md":
            f.write("# " + title)
        elif frmt == "html":
            f.write("<html><body><h1>{t}</h1><ul>\n".format(
                t=title
            ))

        for instr in _CORE_INSTRUCTIONS:
            if frmt == "md":
                f.write(_generate_instruction_markdown(instr) + "\n")
            elif frmt == "html":
                f.write(_generate_instruction_html(instr) + "\n")

        if frmt == "html":
            f.write("\n</ul></body></html>")


def _get_cli_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "command",
        choices=[
            "instructions",
        ]
    )
    parser.add_argument(
        "format",
        choices=[
            "md",
            "html",
        ],
        default="markdown"
    )
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    args = _get_cli_args()
    if args.command == "instructions":
        _generate_instruction_set_documentation(args.format)
