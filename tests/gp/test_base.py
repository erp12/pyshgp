import unittest

from pyshgp.gp.base import PyshBase
from pyshgp.gp.variation import VariationOperator


class TestPyshBase(unittest.TestCase):

    def setUp(self):
        self.b = PyshBase(population_size=10)

    def test_choose_genetic_operator(self):
        op = self.b.choose_genetic_operator()
        self.assertTrue(isinstance(op, VariationOperator))

    def test_make_spawner(self):
        self.b.make_spawner(3)
        self.assertTrue(hasattr(self.b, 'spawner'))

    def test_init_population(self):
        self.b.make_spawner(3)
        self.b.init_population()
        self.assertTrue(hasattr(self.b, 'population'))
        self.assertEqual(len(self.b.population), 10)
