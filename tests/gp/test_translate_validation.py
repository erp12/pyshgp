from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.gp.genome import genome_to_code
from tests.support import load_code, load_genome


def check_translation(program_name: str, interpreter: PushInterpreter):
    genome = load_genome(program_name, interpreter)
    prog = load_code(program_name, interpreter)
    assert genome_to_code(genome) == prog


def check_unary_fn_translation(program_name: str):
    interpreter = PushInterpreter(InstructionSet(register_core=True))
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
