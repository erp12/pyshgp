import json

from pyshgp.push.atoms import CodeBlock, Closer, Literal, JitInstructionRef
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.gp.genome import Genome, genome_to_code


def _deserialize_atoms(lst, instr_set: InstructionSet):
    type_lib = instr_set.type_library
    atoms = []
    for atom_spec in lst:
        atom = None
        if isinstance(atom_spec, list):
            atom = CodeBlock(*_deserialize_atoms(atom_spec, instr_set))
        else:
            atom_type = atom_spec["a"]
            if atom_type == "close":
                atom = Closer()
            elif atom_type == "lit":
                push_type = type_lib[atom_spec["t"]]
                value = push_type.coerce(atom_spec["v"])
                atom = Literal(value, push_type)
            elif atom_type == "instr":
                atom = instr_set[atom_spec["n"]]
            elif atom_type == "jit-instr":
                atom = JitInstructionRef(atom_spec["n"])
            else:
                raise ValueError("bad atom spec {s}".format(s=atom_spec))
        atoms.append(atom)
    return atoms


def load_code(name, interpreter) -> CodeBlock:
    with open("tests/resources/programs/" + name + ".json") as f:
        atoms = _deserialize_atoms(json.load(f), interpreter.instruction_set)
        return CodeBlock(*atoms)


def load_genome(name, interpreter) -> Genome:
    with open("tests/resources/genomes/" + name + ".json") as f:
        atoms = _deserialize_atoms(json.load(f), interpreter.instruction_set)
        return Genome.create(atoms)


def check_translation(program_name: str, interpreter: PushInterpreter):
    genome = load_genome(program_name, interpreter)
    prog = load_code(program_name, interpreter)
    assert genome_to_code(genome) == prog


def check_unary_fn_translation(program_name: str):
    interpreter = PushInterpreter(InstructionSet(register_core=True).register_n_inputs(1))
    check_translation(program_name, interpreter)


def test_genome_relu_1():
    check_unary_fn_translation("relu_via_max")


def test_genome_relu_2():
    check_unary_fn_translation("relu_via_if")


def test_genome_fibonacci():
    check_unary_fn_translation("fibonacci")


def test_genome_rswn():
    check_unary_fn_translation("replace_space_with_newline")


def test_genome_point_dist(point_instr_set):
    check_translation("point_distance", PushInterpreter(point_instr_set))
