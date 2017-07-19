from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
import unittest

from pyshgp.gp.evaluate import (evaluate_with_function,
                                evaluate_for_regression,
                                evaluate_for_classification)
from pyshgp.gp.population import Individual
from pyshgp.push.random import PushSpawner


class TestEvaluateFunctions(unittest.TestCase):

    def setUp(self):
        self.atom_gens = [
            lambda: np.random.random(),
        ]
        self.R = PushSpawner(self.atom_gens)
        self.gn = self.R.random_plush_genome(1)
        self.individual = Individual(self.gn)

    def test_evaluate_with_function(self):
        def ef(program): return [1, 2, 3]
        i = evaluate_with_function(self.individual, ef)
        self.assertTrue(hasattr(i, 'error_vector'))

    def test_evaluate_for_regression(self):
        X = np.array([[1, 2], [3, 4]])
        y = np.array([3, 7])
        i = evaluate_for_regression(self.individual, X, y)
        self.assertTrue(hasattr(i, 'total_error'))

    def evaluate_for_classification(self):
        X = np.array([[1, 2], [3, 4]])
        y = np.array([3, 7])
        i = evaluate_for_classification(self.individual, X, y)
        self.assertTrue(hasattr(i, 'total_error'))
