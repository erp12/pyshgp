import unittest
import pyshgp.push.registered_instructions as ri
from pyshgp.push.instruction import PyshInstruction


class TestRegisteredInstructions(unittest.TestCase):

    def test_get_instruction_strd(self):
        add_instr = ri.get_instruction('_integer_add')
        self.assertIsInstance(add_instr, PyshInstruction)

    def test_get_instruction_invd(self):
        self.assertRaises(ValueError, ri.get_instruction, '_foo_bar')

    def get_instructions_by_pysh_type_strd(self):
        l = ri.get_instructions_by_pysh_type('_boolean')
        self.assertIsInstance(l, list)
        self.assertTrue(len(l) > 0)
        self.assertIsInstance(l[0], PyshInstruction)

    def get_instructions_by_pysh_type_invd(self):
        l = ri.get_instructions_by_pysh_type('_foo_bar')
        self.assertEqual(l, [])
