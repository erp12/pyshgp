import unittest

import pyshgp.push.plush as plush


class TestStackMethods(unittest.TestCase):

    def setUp(self):
        self.lit_gene = plush.Gene(7, True, 0, False)

    def test_gene(self):
        self.lit_gene.__repr__()
