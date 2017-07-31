import numpy as np
import unittest

from pyshgp.gp.simplification import (silent_n_random_genes, simplify_once,
                                      noop_n_random_genes, simplify_by_dataset,
                                      simplify_by_function)
from pyshgp.gp.population import Individual
from pyshgp.push.random import PushSpawner


class TestSimplificationFunctions(unittest.TestCase):

    def setUp(self):
        self.atom_gens = [
            lambda: np.random.random(),
        ]
        self.R = PushSpawner(self.atom_gens)
        self.gn = self.R.random_plush_genome(1)
        self.individual = Individual(self.gn)

    def test_silent_n_random_genes(self):
        silent_n_random_genes(self.gn, 1)
        self.assertTrue(self.gn[0].is_silent)

    def test_noop_n_random_genes(self):
        noop_n_random_genes(self.gn, 1)
        self.assertTrue(self.gn[0].atom.name == '_exec_noop')

    def test_simplify_once(self):
        self.gn = simplify_once(self.gn)
        a = self.gn[0].is_silent
        b = (hasattr(self.gn[0].atom, 'name') and
             self.gn[0].atom.name == '_exec_noop')
        self.assertTrue(a or b)

    def test_simplify_by_dataset(self):
        simplify_by_dataset(self.individual, np.array([[0, 0], [0, 0]]),
                            np.array([0, 0]), 'regression')

    def test_simplify_by_function(self):
        simplify_by_function(self.individual, lambda s: [0, 0, 0])
