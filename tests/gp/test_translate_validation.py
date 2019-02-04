from pyshgp.push.atoms import CodeBlock
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.gp.genome import Genome


# Not using fixture in order to spot unintentional updates during execution.
i_set = InstructionSet(register_all=True).register_n_inputs(10)


def load_genome(name: str) -> Genome:
    with open("tests/resources/genomes/" + name + ".json") as f:
        return Genome.from_json_str(f.read(), i_set)


def load_program(name: str) -> CodeBlock:
    with open("tests/resources/programs/" + name + ".json") as f:
        return CodeBlock.from_json_str(f.read(), i_set)


def test_genome_relu_1(interpreter: PushInterpreter):
    name = "relu_via_max"
    genome = load_genome(name)
    prog = load_program(name)
    assert genome.to_code_block() == prog


def test_genome_relu_2(interpreter: PushInterpreter):
    name = "relu_via_if"
    genome = load_genome(name)
    prog = load_program(name)
    assert genome.to_code_block() == prog


def test_genome_fibonacci(interpreter: PushInterpreter):
    name = "fibonacci"
    genome = load_genome(name)
    prog = load_program(name)
    print(genome.to_code_block())
    print(prog)
    assert genome.to_code_block() == prog


def test_genome_rswn(interpreter: PushInterpreter):
    name = "replace_space_with_newline"
    genome = load_genome(name)
    prog = load_program(name)
    assert genome.to_code_block() == prog
