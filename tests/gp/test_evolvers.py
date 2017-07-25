from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
import unittest

from pyshgp.gp.evolvers import (SimplePushGPEvolver, PushGPRegressor,
                                PushGPClassifier)


class TestSimplePushGPEvolverMethods(unittest.TestCase):

    def setUp(self):
        self.evo = SimplePushGPEvolver(max_generations=3, population_size=5,
                                       simplification_steps=50)
        self.ef = lambda s: [np.random.random(), np.random.random()]

    def test_fit(self):
        self.evo.fit(self.ef, 1, ['_float'])
        self.assertTrue(hasattr(self.evo, 'best_'))

    def test_predict(self):
        self.evo.fit(self.ef, 1, ['_float'])
        X = [[1.1], [2.2]]
        predictions = self.evo.predict(X)
        self.assertIsInstance(predictions, np.ndarray)


class TestPushGPRegressorMethods(unittest.TestCase):

    def setUp(self):
        self.X = np.arange(20).reshape(-1, 2)
        self.y = np.arange(10)
        self.evo = PushGPRegressor(max_generations=3, population_size=5,
                                   simplification_steps=50)

    def test_fit(self):
        self.evo.fit(self.X, self.y)
        self.assertTrue(hasattr(self.evo, 'best_'))

    def test_predict(self):
        self.evo.fit(self.X, self.y)
        predictions = self.evo.predict(self.X)
        self.assertIsInstance(predictions, np.ndarray)


class TestPushGPClassifierMethods(unittest.TestCase):

    def setUp(self):
        self.X = np.arange(20).reshape(-1, 2)
        self.y = np.array([1, 0] * 5)
        self.evo = PushGPClassifier(max_generations=3, population_size=5,
                                    simplification_steps=50)

    def test_fit(self):
        self.evo.fit(self.X, self.y)
        self.assertTrue(hasattr(self.evo, 'best_'))

    def test_predict(self):
        self.evo.fit(self.X, self.y)
        predictions = self.evo.predict(self.X)
        self.assertIsInstance(predictions, np.ndarray)
