from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import pyshgp.utils as u
import pyshgp.push.stack as stack

class TestStackMethods(unittest.TestCase):

    def setUp(self):
        self.stck = stack.PyshStack('_integer')

    def test_push(self):
        self.stck.push(7)
        self.assertEqual(len(self.stck), 1)
        self.assertEqual(self.stck[0], 7)

    def test_pop(self):
        self.stck.push(7)
        self.stck.pop()
        self.assertEqual(len(self.stck), 0)

    def test_top_item_A(self):
        self.stck.push(7)
        i = self.stck.top_item()
        self.assertEqual(i, 7)

    def test_top_item_B(self):
        i = self.stck.top_item()
        self.assertIsInstance(i, u.NoStackItem)

    def test_ref(self):
        self.stck.push("a")
        self.stck.push("b")
        self.stck.push("c")
        c = self.stck.ref(0)
        b = self.stck.ref(1)
        a = self.stck.ref(2)
        self.assertEqual(a, "a")
        self.assertEqual(b, "b")
        self.assertEqual(c, "c")

    def test_insert(self):
        self.stck.insert(0, "c")
        self.stck.insert(1, "b")
        self.stck.insert(2, "a")
        c = self.stck.ref(0)
        b = self.stck.ref(1)
        a = self.stck.ref(2)
        self.assertEqual(a, "a")
        self.assertEqual(b, "b")
        self.assertEqual(c, "c")

    def test_flush(self):
        self.stck.push("a")
        self.stck.push("b")
        self.stck.flush()
        self.assertEqual(len(self.stck), 0)
