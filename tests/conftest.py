import pytest
import random
from math import pow, sqrt

from pyshgp.push.type_library import PushTypeLibrary
from pyshgp.push.types import Char, PushInt, PushBool, PushFloat, PushStr
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.instruction import SimpleInstruction
from pyshgp.push.atoms import Closer, Literal
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.state import PushState
from pyshgp.gp.genome import Genome, GeneSpawner


@pytest.fixture(scope="session")
def core_type_lib():
    return PushTypeLibrary(register_core=True)


@pytest.fixture(scope="session")
def instr_set():
    return InstructionSet(register_core=True)


@pytest.fixture(scope="function")
def atoms(instr_set):
    return {
        "5": Literal(5, PushInt),
        "1.2": Literal(1.2, PushFloat),
        "true": Literal(True, PushBool),
        "add": instr_set["int_add"],
        "sub": instr_set["int_sub"],
        "if": instr_set["exec_if"],
        "close": Closer()
    }


@pytest.fixture(scope="function")
def state():
    return PushState(PushTypeLibrary(PushInt, PushBool, PushFloat, PushStr))


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
    l_set = [5, 1.2, True]
    return GeneSpawner(i_set, l_set, [random.random])


# Custom Types

class Point:

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

@pytest.fixture(scope="session")
def point_cls():
    return Point


def to_point(thing):
    return Point(float(thing[0]), float(thing[1]))


@pytest.fixture(scope="session")
def to_point_func():
    return to_point


def point_distance(p1, p2):
    delta_x = p2.x - p1.x
    delta_y = p2.y - p1.y
    return sqrt(pow(delta_x, 2.0) + pow(delta_y, 2.0))


@pytest.fixture(scope="session")
def point_distance_insrt():
    return SimpleInstruction(
        "point_dist", point_distance,
        ["point", "point"], ["float"], 0
    )
