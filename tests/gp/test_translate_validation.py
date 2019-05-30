import json

from pyshgp.push.atoms import CodeBlock, Closer, Literal, JitInstructionRef
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.gp.genome import Genome


def _pysh_collection_from_list(lst, cls, instr_set: InstructionSet) -> CodeBlock:
    type_lib = instr_set.type_library
    gn = Genome()
    for atom_spec in lst:
        atom = None
        if isinstance(atom_spec, list):
            atom = _pysh_collection_from_list(atom_spec, cls, instr_set)
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
        gn.append(atom)
    return gn


def load_program(name, interpreter) -> CodeBlock:
    with open("tests/resources/programs/" + name + ".json") as f:
        return _pysh_collection_from_list(json.load(f), CodeBlock, interpreter.instruction_set)


def load_genome(name, interpreter) -> Genome:
    with open("tests/resources/genomes/" + name + ".json") as f:
        return _pysh_collection_from_list(json.load(f), Genome, interpreter.instruction_set)


def test_genome_relu_1():
    interpreter = PushInterpreter(InstructionSet(register_core=True).register_n_inputs(1))
    name = "relu_via_max"
    genome = load_genome(name, interpreter)
    prog = load_program(name, interpreter)
    assert genome.to_code_block() == prog


def test_genome_relu_2():
    interpreter = PushInterpreter(InstructionSet(register_core=True).register_n_inputs(1))
    name = "relu_via_if"
    genome = load_genome(name, interpreter)
    prog = load_program(name, interpreter)
    assert genome.to_code_block() == prog


def test_genome_fibonacci():
    interpreter = PushInterpreter(InstructionSet(register_core=True).register_n_inputs(1))
    name = "fibonacci"
    genome = load_genome(name, interpreter)
    prog = load_program(name, interpreter)
    assert genome.to_code_block() == prog


def test_genome_rswn():
    interpreter = PushInterpreter(InstructionSet(register_core=True).register_n_inputs(1))
    name = "replace_space_with_newline"
    genome = load_genome(name, interpreter)
    prog = load_program(name, interpreter)
    assert genome.to_code_block() == prog


def test_genome_point_dist(point_instr_set):
    interpreter = PushInterpreter(point_instr_set)
    name = "point_distance"
    genome = load_genome(name, interpreter)
    prog = load_program(name, interpreter)
    assert genome.to_code_block() == prog
