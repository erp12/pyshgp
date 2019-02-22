import pytest
import random

from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.atoms import Closer, Literal
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.state import PushState
from pyshgp.gp.genome import Genome, GeneSpawner


@pytest.fixture(scope="session")
def instr_set():
    return InstructionSet(register_all=True)


@pytest.fixture(scope="function")
def atoms(instr_set):
    return {
        "5": Literal(5),
        "1.2": Literal(1.2),
        "true": Literal(True),
        "add": instr_set["int_add"],
        "sub": instr_set["int_sub"],
        "if": instr_set["exec_if"],
        "close": Closer()
    }


@pytest.fixture(scope="function")
def state():
    return PushState({"int", "float", "bool", "str"})


@pytest.fixture(scope="function")
def interpreter():
    return PushInterpreter()


@pytest.fixture(scope="function")
def simple_genome(atoms):
    return Genome([atoms["5"], atoms["5"], atoms["add"]])


@pytest.fixture(scope="function")
def simple_gene_spawner(atoms):
    i_set = InstructionSet()
    i_set.register_list([atoms["add"], atoms["sub"], atoms["if"]])
    l_set = [atoms["5"], atoms["1.2"], atoms["true"]]
    return GeneSpawner(i_set, l_set, [random.random])
