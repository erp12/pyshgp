from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

import unittest

from pyshgp.gp.base import PyshMixin, SimplePushGPEvolver, PushGPRegressor
from pyshgp.gp.variation import VariationOperator

class TestPyshMixinMethods(unittest.TestCase):

    def test_init_executor(self):
        mixin = PyshMixin(n_jobs=-1)
        mixin.init_executor()
        self.assertTrue(hasattr(mixin, 'pool'))

    def test_choose_genetic_operator(self):
        mixin = PyshMixin()
        op = mixin.choose_genetic_operator()
        self.assertTrue(isinstance(op, VariationOperator))

    def test_make_spawner(self):
        mixin = PyshMixin()
        mixin.make_spawner(3, {'a':0.0})
        self.assertTrue(hasattr(mixin, 'spawner'))

    def test_init_population(self):
        mixin = PyshMixin()
        mixin.make_spawner(3, {})
        op = mixin.init_population()
        self.assertTrue(hasattr(mixin, 'population'))
        self.assertEqual(len(mixin.population), 300)

class TestSimplePushGPEvolverMethods(unittest.TestCase):

    def setUp(self):
        self.reg = SimplePushGPEvolver(max_generations=3, population_size=5)
        self.ef = lambda s: [np.random.random(), np.random.random()]

    def test_fit(self):
        self.reg.fit(self.ef, 0, {})
        self.assertTrue(hasattr(self.reg, 'best_'))
