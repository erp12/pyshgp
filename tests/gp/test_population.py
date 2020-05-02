import pytest
import numpy as np

from pyshgp.gp.population import Population
from pyshgp.gp.individual import Individual
from pyshgp.gp.genome import Genome
from pyshgp.gp.evaluation import DatasetEvaluator
from pyshgp.push.program import ProgramSignature


@pytest.fixture(scope="function")
def simple_individuals(atoms, push_config):
    sig = ProgramSignature(0, ["int"], push_config)
    return [
        Individual(Genome([]), sig),
        Individual(Genome([atoms["5"]]), sig),
        Individual(Genome([atoms["5"], atoms["close"]]), sig),
        Individual(Genome([atoms["5"]]), sig),
    ]


@pytest.fixture(scope="function")
def unevaluated_pop(simple_individuals):
    return Population(simple_individuals)


@pytest.fixture(scope="function")
def partially_evaluated_pop(simple_individuals):
    simple_individuals[0].error_vector = np.array([1, 2, 3])
    simple_individuals[2].error_vector = np.array([0, 0, 0])
    return Population(simple_individuals)


@pytest.fixture(scope="function")
def evaluated_pop(simple_individuals):
    for i in simple_individuals:
        i.error_vector = np.arange(3)
    return Population(simple_individuals)


class TestPopulation:

    def test_unevaluated_population_len(self, unevaluated_pop):
        assert len(unevaluated_pop) == 4

    def test_evaluated_population_len(self, evaluated_pop):
        assert len(evaluated_pop) == 4

    def test_partially_evaluated_population_len(self, partially_evaluated_pop):
        assert len(partially_evaluated_pop) == 4

    def test_empty_population_len(self):
        assert len(Population()) == 0

    def test_partially_evaluated_population_nth(self, partially_evaluated_pop):
        assert int(partially_evaluated_pop[0].total_error) == 0.0
        assert int(partially_evaluated_pop[1].total_error) == 6
        assert partially_evaluated_pop[2].total_error is None
        assert partially_evaluated_pop[3].total_error is None

    def test_add_unevaluated(self, partially_evaluated_pop, simple_program_signature):
        partially_evaluated_pop.add(Individual(Genome([]), simple_program_signature))
        assert len(partially_evaluated_pop) == 5
        assert len(partially_evaluated_pop.unevaluated) == 3

    def test_add_evaluated(self, partially_evaluated_pop, simple_program_signature):
        i = Individual(Genome([]), simple_program_signature)
        i.error_vector = np.array([0, 1, 0])
        partially_evaluated_pop.add(i)
        assert len(partially_evaluated_pop) == 5
        assert len(partially_evaluated_pop.evaluated) == 3

    def test_best(self, partially_evaluated_pop, simple_program_signature):
        i = Individual(Genome([]), simple_program_signature)
        i.error_vector = np.array([0, 1, 0])
        partially_evaluated_pop.add(i)
        assert partially_evaluated_pop.best().total_error == 0.0

    def test_best_n(self, partially_evaluated_pop):
        best_two = partially_evaluated_pop.best_n(2)
        assert best_two[0].total_error == 0.0
        assert best_two[1].total_error == 6

    def test_evaluated_population(self, unevaluated_pop):
        evaluator = DatasetEvaluator(
            [[1], [2], [3]],
            [10, 5, 10]
        )
        unevaluated_pop.evaluate(evaluator)
        a = unevaluated_pop.all_error_vectors()
        e = np.array([
            [5, 0, 5],
            [5, 0, 5],
            [5, 0, 5],
            [evaluator.penalty, evaluator.penalty, evaluator.penalty],
        ])
        assert np.all(np.equal(a, e))

    def test__all_error_vectors(self, partially_evaluated_pop):
        a = partially_evaluated_pop.all_error_vectors()
        e = np.array([
            [0, 0, 0],
            [1, 2, 3]
        ])
        assert np.all(np.equal(a, e))

    def test__all_total_errors(self, partially_evaluated_pop):
        a = partially_evaluated_pop.all_total_errors()
        e = np.array([0, 6])
        assert np.all(np.equal(a, e))

    def test_median_error(self, partially_evaluated_pop):
        assert float(partially_evaluated_pop.median_error()) == 3

    @pytest.mark.filterwarnings("ignore:.*:RuntimeWarning")
    def test_median_error_empty_pop(self):
        assert np.isnan(Population().median_error()).all()

    def test_error_diversity(self, partially_evaluated_pop):
        assert partially_evaluated_pop.error_diversity() == 0.5

    def test_error_diversity_empty_pop(self):
        with pytest.raises(ValueError):
            Population().error_diversity()

    def test_genome_diversity(self, partially_evaluated_pop):
        assert partially_evaluated_pop.genome_diversity() == 0.75

    def test_genome_diversity_empty_pop(self):
        with pytest.raises(ZeroDivisionError):
            Population().genome_diversity()
