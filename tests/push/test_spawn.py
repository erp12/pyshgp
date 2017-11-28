import numpy as np
import unittest

from pyshgp.push.spawn import Spawner
import pyshgp.push.plush as pl
from pyshgp.push.instruction import Instruction


class TestSpawnMethods(unittest.TestCase):

    def setUp(self):
        self.atom_gens = [
            Instruction("noop", lambda s: s, [], 0),
            lambda: np.random.random()
        ]
        self.R = Spawner(self.atom_gens)

    def test_generate_close_count(self):
        c = self.R.generate_close_count()
        self.assertIsInstance(c, int)
        self.assertTrue(c <= 3)
        self.assertTrue(c >= 0)

    def test_atom_to_plush_gene(self):
        a = self.atom_gens[0]
        g = self.R.atom_to_plush_gene(a)
        self.assertIsInstance(g, pl.Gene)

    def test_random_plush_gene(self):
        self.assertIsInstance(self.R.random_plush_gene(), pl.Gene)

    def test_random_plush_genome_with_size(self):
        gn = self.R.random_plush_genome_with_size(5)
        self.assertEqual(len(gn), 5)
        self.assertIsInstance(gn[0], pl.Gene)

    def test_random_plush_genome(self):
        gn = self.R.random_plush_genome(5)
        self.assertTrue(len(gn) <= 5)
        self.assertTrue(len(gn) > 0)
        self.assertIsInstance(gn[0], pl.Gene)
