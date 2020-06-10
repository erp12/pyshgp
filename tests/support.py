import json

from pyshgp.gp.genome import Genome
from pyshgp.push.atoms import CodeBlock, Closer, Literal, InstructionMeta, Input
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.program import ProgramSignature, Program


def _deserialize_atoms(lst, instr_set: InstructionSet):
    type_lib = instr_set.type_library
    atoms = []
    for atom_spec in lst:
        atom = None
        if isinstance(atom_spec, list):
            atom = CodeBlock(_deserialize_atoms(atom_spec, instr_set))
        else:
            atom_type = atom_spec["a"]
            if atom_type == "close":
                atom = Closer()
            elif atom_type == "lit":
                push_type = type_lib[atom_spec["t"]]
                value = push_type.coerce(atom_spec["v"])
                atom = Literal(value=value, push_type=push_type)
            elif atom_type == "input":
                atom = Input(input_index=atom_spec["i"])
            elif atom_type == "instr":
                instr = instr_set[atom_spec["n"]]
                atom = InstructionMeta(name=instr.name, code_blocks=instr.code_blocks)
            else:
                raise ValueError("bad atom spec {s}".format(s=atom_spec))
        atoms.append(atom)
    return atoms


def load_code(name, interpreter) -> CodeBlock:
    with open("tests/resources/programs/" + name + ".json") as f:
        atoms = _deserialize_atoms(json.load(f), interpreter.instruction_set)
        return CodeBlock(atoms)


def get_program(name: str, sig: ProgramSignature, interpreter: PushInterpreter):
    cb = load_code(name, interpreter)
    return Program(code=cb, signature=sig)


def load_genome(name, interpreter) -> Genome:
    with open("tests/resources/genomes/" + name + ".json") as f:
        atoms = _deserialize_atoms(json.load(f), interpreter.instruction_set)
        return Genome(atoms)
