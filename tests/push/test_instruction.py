from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import unittest

from pyshgp.push.interpreter import PushState
from pyshgp.push.instruction import (PyshInputInstruction,
                                     PyshSetOutputInstruction,
                                     PyshReduceOutputInstruction,
                                     PyshTweakOutputInstruction,
                                     make_numeric_output_instructions,
                                     make_classification_instructions)


class TestInstructionMethods(unittest.TestCase):

    def setUp(self):
        self.state = PushState([1, 2], ['_exec'])
        self.in0 = PyshInputInstruction(0)
        self.in1 = PyshInputInstruction(1)
        self.set_out_instr = PyshSetOutputInstruction(0, '_exec')

        def add(x, y): return x + y
        self.red_out_instr = PyshReduceOutputInstruction(0, '_exec', add, '+')

        def inc(x): return x + 5
        self.twk_out_instr = PyshTweakOutputInstruction(0, inc, '+5')

    def test_input_execute(self):
        self.in0.execute(self.state)
        self.assertEqual(self.state['_exec'][0], 2)

    def test_set_output_execute(self):
        self.in0.execute(self.state)
        self.set_out_instr.execute(self.state)
        self.assertEqual(self.state.outputs, [2])

    def test_reduce_output_execute(self):
        self.in0.execute(self.state)
        self.set_out_instr.execute(self.state)
        self.in1.execute(self.state)
        self.red_out_instr.execute(self.state)
        self.assertEqual(self.state.outputs, [3])

    def test_reduce_output_execute_2(self):
        self.in1.execute(self.state)
        self.red_out_instr.execute(self.state)
        self.assertEqual(self.state.outputs, [1])

    def test_tweak_output_execute(self):
        self.in0.execute(self.state)
        self.set_out_instr.execute(self.state)
        self.twk_out_instr.execute(self.state)
        self.assertEqual(self.state.outputs, [7])

    def test_make_numeric_output_instructions_int(self):
        instrs = make_numeric_output_instructions(0, True)
        self.assertEqual(len(instrs), 2)
        self.assertIsInstance(instrs[0], PyshSetOutputInstruction)
        self.assertIsInstance(instrs[1], PyshReduceOutputInstruction)

    def test_make_numeric_output_instructions_float(self):
        instrs = make_numeric_output_instructions(0)
        self.assertEqual(len(instrs), 4)
        self.assertIsInstance(instrs[0], PyshSetOutputInstruction)
        self.assertIsInstance(instrs[1], PyshReduceOutputInstruction)
        self.assertIsInstance(instrs[2], PyshSetOutputInstruction)
        self.assertIsInstance(instrs[3], PyshReduceOutputInstruction)

    def test_make_classification_instructions(self):
        instrs = make_classification_instructions(0)
        self.assertEqual(len(instrs), 6)
        self.assertIsInstance(instrs[0], PyshSetOutputInstruction)
        self.assertIsInstance(instrs[1], PyshSetOutputInstruction)
        self.assertIsInstance(instrs[2], PyshReduceOutputInstruction)
        self.assertIsInstance(instrs[3], PyshReduceOutputInstruction)
        self.assertIsInstance(instrs[4], PyshTweakOutputInstruction)
        self.assertIsInstance(instrs[5], PyshTweakOutputInstruction)
