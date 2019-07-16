import pytest

from pyshgp.gp.search import SearchConfiguration
from pyshgp.gp.evaluation import DatasetEvaluator


@pytest.fixture(scope="session")
def empty_evaluator():
    return DatasetEvaluator([], [])


class TestSearchConfiguration:

    def test_create_config_strs(self, empty_evaluator, simple_gene_spawner):
        config = SearchConfiguration(
            empty_evaluator,
            simple_gene_spawner,
            "tournament",
            "alternation",
            tournament_size=14,
            alignment_deviation=5
        )
        assert config.get_selector().tournament_size == 14
        assert config.get_variation_op().alignment_deviation == 5


# @TODO: TEST - Test with custom PushTypeLibrary and custom instructions.
