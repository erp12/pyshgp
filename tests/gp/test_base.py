from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

import unittest

from pyshgp.gp.base import PyshMixin, SimplePushGPEvolver, PushGPRegressor
from pyshgp.gp.variation import VariationOperator
from pyshgp.utils import is_float_type

class TestPyshMixinMethods(unittest.TestCase):

    def setUp(self):
        self.mixin = PyshMixin()

    def test_choose_genetic_operator(self):
        op = self.mixin.choose_genetic_operator()
        self.assertTrue(isinstance(op, VariationOperator))

    def test_make_spawner(self):
        self.mixin.make_spawner(3, {'a': 0.0})
        self.assertTrue(hasattr(self.mixin, 'spawner'))

    def test_init_population(self):
        self.mixin.make_spawner(3, {})
        self.mixin.init_population()
        self.assertTrue(hasattr(self.mixin, 'population'))
        self.assertEqual(len(self.mixin.population), 300)


class TestSimplePushGPEvolverMethods(unittest.TestCase):

    def setUp(self):
        self.evo = SimplePushGPEvolver(max_generations=3, population_size=5,
                                       simplification_steps=50)
        self.ef = lambda s: [np.random.random(), np.random.random()]

    def test_evaluate_with_function(self):
        self.evo.make_spawner(3, {'a': 0.0})
        self.evo.init_population()
        self.evo.evaluate_with_function(self.ef)
        self.assertTrue(hasattr(self.evo.population[0], 'total_error'))
        self.assertTrue(hasattr(self.evo.population[1], 'total_error'))
        self.assertTrue(hasattr(self.evo.population[2], 'total_error'))

    def test_fit(self):
        self.evo.fit(self.ef, 0, {})
        self.assertTrue(hasattr(self.evo, 'best_'))


class TestPushGPRegressorMethods(unittest.TestCase):

    def setUp(self):
        self.X = np.arange(20).reshape(-1, 2)
        self.y = np.arange(10).reshape(-1, 1)
        self.evo = PushGPRegressor(max_generations=3, population_size=5,
                                   simplification_steps=50)

    def test_evaluate(self):
        self.evo.make_spawner(2, {'pred': 0.0})
        self.evo.init_population()
        self.evo.evaluate(self.X, self.y)
        self.assertTrue(hasattr(self.evo.population[0], 'total_error'))
        self.assertTrue(hasattr(self.evo.population[1], 'total_error'))
        self.assertTrue(hasattr(self.evo.population[2], 'total_error'))
        self.assertTrue(is_float_type(self.evo.population[0].total_error))
        self.assertTrue(is_float_type(self.evo.population[1].total_error))
        self.assertTrue(is_float_type(self.evo.population[2].total_error))

    def test_fit(self):
        self.evo.fit(self.X, self.y)
        self.assertTrue(hasattr(self.evo, 'best_'))
