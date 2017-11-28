import unittest

from pyshgp.push.spawn import Spawner
import pyshgp.push.translation as t


class TestTranslateMethods(unittest.TestCase):

    def setUp(self):
        self.balenced = ["_open", 1, "_close", "_open", 2, "_close"]
        self.unbal = ["_open", "_open", 1, "_close", "_close", 3, "_close"]
        R = Spawner([lambda: 0])
        self.gn = R.random_plush_genome_with_size(5)

    def test_get_matcing_close_index(self):
        i = t.get_matcing_close_index(self.unbal)
        self.assertEqual(i, 4)

    def test_open_close_sequence_to_list(self):
        lst = t.open_close_sequence_to_list(self.balenced)
        self.assertEqual(lst, [[1], [2]])

    def test_genome_to_program(self):
        p = t.genome_to_program(self.gn)
        self.assertIsInstance(p, list)
        self.assertEqual(len(self.gn), 5)
