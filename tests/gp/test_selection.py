import pytest
import numpy as np

from pyshgp.gp.selection import FitnessProportionate, Tournament, Lexicase, Elite
from pyshgp.gp.population import Population
from pyshgp.gp.individual import Individual
from pyshgp.gp.genome import Genome
from pyshgp.push.interpreter import ProgramSignature


@pytest.fixture(scope="function")
def population(atoms, push_config):
    gn = Genome()
    sig = ProgramSignature(0, [], push_config)
    i1 = Individual(gn, sig)
    i1.error_vector = np.array([0, 20, 0])  # 20

    i2 = Individual(gn, sig)
    i2.error_vector = np.array([3, 3, 3])  # 9

    i3 = Individual(gn, sig)
    i3.error_vector = np.array([1, 2, 3])  # 6

    i4 = Individual(gn, sig)
    i4.error_vector = np.array([4, 3, 5])  # 12

    return Population([i1, i2, i3, i4])


def test_fitness_proportionate(population):
    s = FitnessProportionate()
    assert isinstance(s.select_one(population), Individual)
    assert len(s.select(population, 2)) == 2


def test_tournament(population):
    s = Tournament(2)
    i = s.select_one(population)
    assert i.total_error <= 12


def test_lexicase(population):
    s = Lexicase()
    i = s.select_one(population)
    assert i.total_error == 20 or i.total_error == 6


def test_epsilon_lexicase(population):
    s = Lexicase(1.1)
    i = s.select_one(population)
    assert i.total_error == 20 or i.total_error == 6


def test_elite(population):
    s = Elite()
    i = s.select_one(population)
    assert i.total_error == 6
    best_two = s.select(population, 2)
    assert best_two[0].total_error == 6
    assert best_two[1].total_error == 9
