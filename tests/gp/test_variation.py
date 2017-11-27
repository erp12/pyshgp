import numpy as np
from random import choice
import unittest

import pyshgp.gp.variation as v
import pyshgp.gp.population as p
from pyshgp.push.random import Spawner
from pyshgp.push.registered_instructions import get_instruction


atom_gens = [
    lambda: np.random.random(),
    lambda: np.random.randint(10),
    lambda: choice('abcdefghijklmnopqrstuvwxyz \n!.'),
    get_instruction('_integer_add'),
    get_instruction('_float_add'),
    get_instruction('_string_from_float'),
    get_instruction('_string_from_integer'),
    get_instruction('_string_concat'),
]


class TestPerturbCloseMutationMethods(unittest.TestCase):

    def setUp(self):
        self.R = Spawner(atom_gens)
        self.i1 = p.Individual(self.R.random_plush_genome(15))

    def test_produce(self):
        pim = v.PerturbCloseMutation(rate=0.9)
        child = pim.produce([self.i1], self.R)
        self.assertEqual(len(child.genome), len(self.i1.genome))
        self.assertFalse(hasattr(child, 'total_error'))


class TestPerturbIntegerMutationMethods(unittest.TestCase):

    def setUp(self):
        self.R = Spawner(atom_gens)
        self.i1 = p.Individual(self.R.random_plush_genome(15))

    def test_produce(self):
        pim = v.PerturbIntegerMutation(rate=0.9)
        child = pim.produce([self.i1], self.R)
        self.assertEqual(len(child.genome), len(self.i1.genome))
        self.assertFalse(hasattr(child, 'total_error'))


class TestAlternationMethods(unittest.TestCase):

    def setUp(self):
        self.R = Spawner(atom_gens)
        self.i1 = p.Individual(self.R.random_plush_genome(5))
        self.i2 = p.Individual(self.R.random_plush_genome(5))

    def test_produce(self):
        al = v.Alternation(rate=0.5)
        child = al.produce((self.i1, self.i2))
        self.assertFalse(hasattr(child, 'total_error'))


class TestVariationOperatorPipelineMethods(unittest.TestCase):

    def setUp(self):
        self.R = Spawner(atom_gens)
        self.i1 = p.Individual(self.R.random_plush_genome(5))
        self.i2 = p.Individual(self.R.random_plush_genome(5))

    def test_produce(self):
        al = v.VariationOperatorPipeline(
            (v.Alternation(rate=0.5), v.TweakStringMutation(rate=0.7))
        )
        child = al.produce((self.i1, self.i2), self.R)
        self.assertFalse(hasattr(child, 'total_error'))
