from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

import unittest

from pyshgp.gp.base import PyshMixin, PushGPRegressor
from pyshgp.gp.variation import VariationOperator

# class TestPyshMixinMethods(unittest.TestCase):
#
#     def test_init_executor(self):
#         mixin = PyshMixin(n_jobs=-1)
#         mixin.init_executor()
#         self.assertTrue(hasattr(mixin, 'pool'))
#
#     def test_choose_genetic_operator(self):
#         mixin = PyshMixin()
#         op = mixin.choose_genetic_operator()
#         self.assertTrue(isinstance(op, VariationOperator))
#
#     def test_make_spawner(self):
#         mixin = PyshMixin()
#         mixin.make_spawner(3)
#         self.assertTrue(hasattr(mixin, 'spawner'))
#
#     def test_init_population(self):
#         mixin = PyshMixin()
#         mixin.make_spawner(3)
#         op = mixin.init_population()
#         self.assertTrue(hasattr(mixin, 'population'))
#         self.assertEqual(len(mixin.population), 300)
#
# class TestPyshMixinMethods(unittest.TestCase):
#
#     def setUp(self):
#         self.reg = PushGPRegressor(max_generations=3, population_size=5)
#         target_function = lambda x: x**3 - (2*(x**2)) - x
#         self.X = np.arange(0, 1, 0.1).reshape(-1, 1)
#         self.y = np.array([target_function(x) for x in self.X]).reshape(-1, 1)
#
#     def test_fit(self):
#         self.reg.fit(self.X, self.y)
#         self.assertTrue(hasattr(self.reg, 'best_'))
