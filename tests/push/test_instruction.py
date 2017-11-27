import unittest

from pyshgp.push.interpreter import PushState
from pyshgp.push.instruction import InputInstruction


class TestInstructionMethods(unittest.TestCase):

    def setUp(self):
        self.state = PushState()
        self.state.load_inputs(['a', 'b', 'c'])
        self.in0 = InputInstruction(0)
        self.in1 = InputInstruction(1)

    def test_input_execute(self):
        self.in0.execute(self.state)
        self.assertEqual(self.state['_exec'][0], 'c')
