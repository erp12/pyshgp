import unittest

from pyshgp.push.interpreter import PushState
from pyshgp.push.instruction import PyshInputInstruction


class TestInstructionMethods(unittest.TestCase):

    def setUp(self):
        self.state = PushState([1, 2], ['_exec'])
        self.in0 = PyshInputInstruction(0)
        self.in1 = PyshInputInstruction(1)

    def test_input_execute(self):
        self.in0.execute(self.state)
        self.assertEqual(self.state['_exec'][0], 2)
