import pytest
import numpy as np

from pyshgp.gp.individual import Individual
from pyshgp.gp.genome import Genome
from pyshgp.push.atoms import CodeBlock


@pytest.fixture(scope="function")
def simple_genome(atoms):
    return Genome([atoms["true"], atoms["if"], atoms["1.2"], atoms["close"], atoms["5"]])


@pytest.fixture(scope="function")
def unevaluated_individual(simple_genome):
    return Individual(simple_genome)


class TestIndividual:

    def test_get_program(self, unevaluated_individual):
        p = unevaluated_individual.program
        assert isinstance(p, CodeBlock)

    def test_set_program(self, unevaluated_individual):
        with pytest.raises(AttributeError):
            unevaluated_individual.program = CodeBlock()

    def test_set_error_vector(self, unevaluated_individual):
        assert unevaluated_individual.total_error is None
        unevaluated_individual.error_vector = np.arange(5)
        assert len(unevaluated_individual.error_vector) == 5
        assert unevaluated_individual.total_error == 10

    def test_set_error_vector_w_inf(self, unevaluated_individual):
        assert unevaluated_individual.total_error is None
        unevaluated_individual.error_vector = np.array([np.inf, 0, np.inf, np.inf])
        assert len(unevaluated_individual.error_vector) == 4
        assert unevaluated_individual.total_error == np.inf

    def test_set_total_error(self, unevaluated_individual):
        with pytest.raises(AttributeError):
            unevaluated_individual.total_error = 123.45
