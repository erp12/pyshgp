from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from pyshgp.push import instruction as instr

class TestPushStateMethods(unittest.TestCase):

    def test_make_vote_instruction_set(self):
        l = instr.make_vote_instruction_set(['a', 'b'])
        for el in l:
            self.assertIsInstance(el, instr.PyshClassVoteInstruction)
        self.assertEqual(len(l), 16)
