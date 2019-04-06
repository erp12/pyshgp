from pyshgp.push.atoms import CodeBlock
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.gp.genome import Genome


# Not using fixture in order to spot unintentional updates during execution.
i_set = InstructionSet(register_core=True).register_n_inputs(10)


def load_genome(name: str, core_type_lib) -> Genome:
    with open("tests/resources/genomes/" + name + ".json") as f:
        return Genome.from_json_str(f.read(), i_set, core_type_lib)


def load_program(name: str, core_type_lib) -> CodeBlock:
    with open("tests/resources/programs/" + name + ".json") as f:
        return CodeBlock.from_json_str(f.read(), i_set, core_type_lib)


def test_genome_relu_1(interpreter: PushInterpreter, core_type_lib):
    name = "relu_via_max"
    genome = load_genome(name, core_type_lib)
    prog = load_program(name, core_type_lib)
    assert genome.to_code_block() == prog


def test_genome_relu_2(interpreter: PushInterpreter, core_type_lib):
    name = "relu_via_if"
    genome = load_genome(name, core_type_lib)
    prog = load_program(name, core_type_lib)
    assert genome.to_code_block() == prog


def test_genome_fibonacci(interpreter: PushInterpreter, core_type_lib):
    name = "fibonacci"
    genome = load_genome(name, core_type_lib)
    prog = load_program(name, core_type_lib)
    print(genome.to_code_block())
    print(prog)
    assert genome.to_code_block() == prog


def test_genome_rswn(interpreter: PushInterpreter, core_type_lib):
    name = "replace_space_with_newline"
    genome = load_genome(name, core_type_lib)
    prog = load_program(name, core_type_lib)
    assert genome.to_code_block() == prog
