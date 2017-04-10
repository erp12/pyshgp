from __future__ import absolute_import, division, print_function, unicode_literals 

import unittest

import pyshgp.utils as u
import pyshgp.push.random as r
import pyshgp.push.translation as t

class TestTranslateMethods(unittest.TestCase):

    def setUp(self):
        self.balenced = ["_open", 1, "_close", "_open", 2, "_close"]
        self.unbalenced = ["_open", "_open", 1, "_close", "_close", 3, "_close"]
        R = r.Random([lambda: 0])
        self.gn = R.random_plush_genome(5)

    def test_get_matcing_close_index(self):
        i = t.get_matcing_close_index(self.unbalenced)
        self.assertEqual(i, 4)

    def test_open_close_sequence_to_list(self):
        l = t.open_close_sequence_to_list(self.balenced)
        self.assertEqual(l, [[1], [2]])

    def test_genome_to_program(self):
        p = t.genome_to_program(self.gn, 5)
        self.assertIsInstance(p, list)
        self.assertTrue(len(p) <  5)