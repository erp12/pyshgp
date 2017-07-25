from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
import unittest

import pyshgp.gp.population as p
import pyshgp.push.random as r


class TestIndividualMethods(unittest.TestCase):

    def setUp(self):
        self.atom_gens = [
            lambda: np.random.random(),
        ]
        self.R = r.PushSpawner(self.atom_gens)
        self.i = p.Individual(self.R.random_plush_genome_with_size(4))

    def test_run_program(self):
        inputs = [1, 2, 3]
        result = self.i.run_program(inputs, ['_integer'])
        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0])


class TestPopulationMethods(unittest.TestCase):

    def setUp(self):
        self.atom_gens = [lambda: np.random.random()]
        self.R = r.PushSpawner(self.atom_gens)
        self.pop = p.Population()
        self.pop.append(p.Individual(self.R.random_plush_genome(5)))
        self.pop.append(p.Individual(self.R.random_plush_genome(5)))
        self.pop.append(p.Individual(self.R.random_plush_genome(5)))

    def test_pop_evaluate_by_function(self):
        def ef(program): return [1, 2, 3]
        self.pop.evaluate_by_function(ef)
        self.assertEqual(self.pop[0].error_vector, [1, 2, 3])
        self.assertEqual(self.pop[2].error_vector, [1, 2, 3])

    def test_pop_evaluate_by_dataset(self):
        X = np.array([[1, 2], [3, 4]])
        y = np.array([3, 7])
        self.pop.evaluate_by_dataset(X, y, 'regression')
        self.assertTrue(hasattr(self.pop[0], 'error_vector'))
        self.assertTrue(hasattr(self.pop[1], 'error_vector'))
        self.assertTrue(hasattr(self.pop[2], 'error_vector'))
        self.assertIsNotNone(self.pop[0].error_vector)
        self.assertIsNotNone(self.pop[1].error_vector)
        self.assertIsNotNone(self.pop[2].error_vector)

    def test_lexicase(self):
        def ef(program): return [1, 2, 3]
        self.pop.evaluate_by_function(ef)
        parent = self.pop.select(method='lexicase')
        self.assertEqual(parent.error_vector, [1, 2, 3])

    def test_eplexicase(self):
        def ef(program): return [1, 2, 3]
        self.pop.evaluate_by_function(ef)
        parent = self.pop.select(method='epsilon_lexicase')
        self.assertEqual(parent.error_vector, [1, 2, 3])

    def test_tourn(self):
        def ef(program): return [1, 2, 3]
        self.pop.evaluate_by_function(ef)
        parent = self.pop.select(method='tournament')
        self.assertEqual(parent.error_vector, [1, 2, 3])

    def test_lowest_error(self):
        def ef(program): return [np.random.random(), np.random.random()]
        self.pop.evaluate_by_function(ef)
        err = self.pop.lowest_error()
        self.assertTrue(err <= self.pop[0].total_error)
        self.assertTrue(err <= self.pop[1].total_error)
        self.assertTrue(err <= self.pop[2].total_error)

    def test_average_error(self):
        def ef(program): return [np.random.random(), np.random.random()]
        self.pop.evaluate_by_function(ef)
        err = self.pop.average_error()
        self.assertTrue(err < 2)
        self.assertTrue(err > 0)

    def test_unique(self):
        def ef(program): return [np.random.random(), np.random.random()]
        self.pop.evaluate_by_function(ef)
        unique = self.pop.unique()
        self.assertEqual(unique, 3)

    def test_best_program(self):
        def ef(program): return [np.random.random(), np.random.random()]
        self.pop.evaluate_by_function(ef)
        best = self.pop.best_program()
        self.assertIsInstance(best, list)

    def best_program_error_vector(self):
        def ef(program): return [np.random.random(), np.random.random()]
        self.pop.evaluate_by_function(ef)
        best_err = self.pop.best_program_error_vector()
        self.assertIsInstance(best_err, list)
        self.assertEqual(len(best_err), 2)
