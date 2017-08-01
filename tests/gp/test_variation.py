import numpy as np
from random import choice
import unittest

import pyshgp.gp.variation as v
import pyshgp.gp.population as p
import pyshgp.push.random as r
import pyshgp.push.plush as pl
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


class TestPerturbIntegerMutationMethods(unittest.TestCase):

    def setUp(self):
        self.R = r.PushSpawner(atom_gens)
        self.i1 = p.Individual(self.R.random_plush_genome(15))

    def test_produce(self):
        pim = v.PerturbIntegerMutation(rate=0.9)
        child = pim.produce([self.i1], self.R)
        self.assertEqual(len(child.genome), len(self.i1.genome))
        self.assertFalse(hasattr(child, 'total_error'))


class TestUniformMutationMethods(unittest.TestCase):

    def setUp(self):
        self.R = r.PushSpawner(atom_gens)
        self.i1 = p.Individual(self.R.random_plush_genome(5))

    def test_string_tweak(self):
        um = v.UniformMutation()
        new_s = um.string_tweak('a' * 300)
        self.assertTrue(not new_s == 'a' * 300)

    def test_constant_mutator_int(self):
        um = v.UniformMutation()
        g = pl.Gene(10, True, 0, False)
        result = um.constant_mutator(g)
        self.assertTrue(type(result.atom) == int)

    def test_constant_mutator_float(self):
        um = v.UniformMutation()
        g = pl.Gene(100.0, True, 0, False)
        result = um.constant_mutator(g)
        self.assertTrue(not result.atom == 100.0)

    def test_constant_mutator_string(self):
        um = v.UniformMutation()
        g = pl.Gene('a' * 300, True, 0, False)
        result = um.constant_mutator(g)
        self.assertTrue(not result.atom == 'a' * 300)

    def test_constant_mutator_bool(self):
        um = v.UniformMutation()
        g = pl.Gene(True, True, 0, False)
        result = um.constant_mutator(g)
        self.assertIsInstance(result.atom, bool)

    def test_produce(self):
        um = v.UniformMutation(rate=0.9)
        child = um.produce([self.i1], self.R)
        self.assertEqual(len(child.genome), len(self.i1.genome))
        self.assertFalse(hasattr(child, 'total_error'))


class TestAlternationMethods(unittest.TestCase):

    def setUp(self):
        self.R = r.PushSpawner(atom_gens)
        self.i1 = p.Individual(self.R.random_plush_genome(5))
        self.i2 = p.Individual(self.R.random_plush_genome(5))

    def test_produce(self):
        al = v.Alternation(rate=0.5)
        child = al.produce((self.i1, self.i2))
        self.assertFalse(hasattr(child, 'total_error'))


class TestVariationOperatorPipelineMethods(unittest.TestCase):

    def setUp(self):
        self.R = r.PushSpawner(atom_gens)
        self.i1 = p.Individual(self.R.random_plush_genome(5))
        self.i2 = p.Individual(self.R.random_plush_genome(5))

    def test_produce(self):
        al = v.VariationOperatorPipeline(
            (v.Alternation(rate=0.5), v.UniformMutation(rate=0.7))
        )
        child = al.produce((self.i1, self.i2), self.R)
        self.assertFalse(hasattr(child, 'total_error'))
