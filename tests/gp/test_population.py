from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

import unittest

import pyshgp.gp.population as p
import pyshgp.push.random as r
import pyshgp.push.plush as pl
import pyshgp.push.instruction as instr
import pyshgp.push.interpreter as interp

class TestIndividualMethods(unittest.TestCase):

    def setUp(self):
        self.atom_gens = [
            lambda: np.random.random(),
        ]
        self.R = r.PushSpawner(self.atom_gens)
        self.i = p.Individual(self.R.random_plush_genome_with_size(4))

    def test_run_program(self):
        inputs = [1,2,3]
        result = self.i.run_program(inputs, {})
        self.assertEqual(len(result), 0)

    def test_evaluate(self):
        X = np.arange(3).reshape(-1, 1)
        y = np.array([0.5, 0.5, 0.5]).reshape(-1, 1)
        self.i.evaluate(X, y, {'?':-999})

    def test_evaluate_with_function(self):
        ef = lambda program: [1, 2, 3]
        self.i.evaluate_with_function(ef)
        self.assertEqual(self.i.error_vector, [1,2,3])
        self.assertEqual(self.i.total_error, 6)

    def test_simplify(self):
        X = np.arange(3).reshape(-1, 1)
        y = np.array(['a', 'b', 'c']).reshape(-1, 1)
        self.i.simplify(X, y, {'?':-999})
        self.assertEqual(self.i.program, [])
        self.assertEqual(len(self.i.genome), 4)

    def test_simplify_with_function(self):
        ef = lambda program: [1, 2, 3]
        self.i.evaluate_with_function(ef)
        self.i.simplify_with_function(ef)
        self.assertEqual(self.i.program, [])
        self.assertEqual(len(self.i.genome), 4)

class TestPopulationMethods(unittest.TestCase):

    def setUp(self):
        self.atom_gens = [
            lambda: np.random.random(),
        ]
        self.R = r.PushSpawner(self.atom_gens)
        self.pop = p.Population()
        self.pop.append(p.Individual(self.R.random_plush_genome(5)))
        self.pop.append(p.Individual(self.R.random_plush_genome(5)))
        self.pop.append(p.Individual(self.R.random_plush_genome(5)))

    def test_pop_evaluate(self):
        ef = lambda program: [1, 2, 3]
        self.pop.evaluate_with_function(ef)
        self.assertEqual(self.pop[0].error_vector, [1,2,3])
        self.assertEqual(self.pop[2].error_vector, [1,2,3])

    def test_lexicase(self):
        ef = lambda program: [1, 2, 3]
        self.pop.evaluate_with_function(ef)
        parent = self.pop.select(method='lexicase')
        self.assertEqual(parent.error_vector, [1,2,3])

    def test_eplexicase(self):
        ef = lambda program: [1, 2, 3]
        self.pop.evaluate_with_function(ef)
        parent = self.pop.select(method='epsilon_lexicase')
        self.assertEqual(parent.error_vector, [1,2,3])

    def test_tourn(self):
        ef = lambda program: [1, 2, 3]
        self.pop.evaluate_with_function(ef)
        parent = self.pop.select(method='tournament')
        self.assertEqual(parent.error_vector, [1,2,3])

    def test_lowest_error(self):
        ef = lambda program: [np.random.random(), np.random.random()]
        self.pop.evaluate_with_function(ef)
        err = self.pop.lowest_error()
        self.assertTrue(err <= self.pop[0].total_error)
        self.assertTrue(err <= self.pop[1].total_error)
        self.assertTrue(err <= self.pop[2].total_error)

    def test_average_error(self):
        ef = lambda program: [np.random.random(), np.random.random()]
        self.pop.evaluate_with_function(ef)
        err = self.pop.average_error()
        self.assertTrue(err < 2)
        self.assertTrue(err > 0)

    def test_unique(self):
        ef = lambda program: [np.random.random(), np.random.random()]
        self.pop.evaluate_with_function(ef)
        unique = self.pop.unique()
        self.assertEqual(unique, 3)
