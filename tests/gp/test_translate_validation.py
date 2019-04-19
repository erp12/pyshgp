from pyshgp.push.atoms import CodeBlock
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.gp.genome import Genome


# Not using fixture in order to spot unintentional updates during execution.
i_set = InstructionSet(register_core=True).register_n_inputs(10)


def load_genome(name, interpreter) -> Genome:
    with open("tests/resources/genomes/" + name + ".json") as f:
        return Genome.from_json_str(f.read(), interpreter.instruction_set)


def load_program(name, interpreter) -> CodeBlock:
    with open("tests/resources/programs/" + name + ".json") as f:
        return CodeBlock.from_json_str(f.read(), interpreter.instruction_set)


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
