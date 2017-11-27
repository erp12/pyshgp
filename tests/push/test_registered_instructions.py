import unittest
import pyshgp.push.registered_instructions as ri
from pyshgp.push.instruction import Instruction


class TestRegisteredInstructions(unittest.TestCase):

    def test_get_instruction_strd(self):
        add_instr = ri.get_instruction('_integer_add')
        self.assertIsInstance(add_instr, Instruction)

    def test_get_instruction_invd(self):
        self.assertRaises(ValueError, ri.get_instruction, '_foo_bar')

    def get_instructions_by_pysh_type_strd(self):
        lst = ri.get_instructions_by_pysh_type('_boolean')
        self.assertIsInstance(lst, list)
        self.assertTrue(len(lst) > 0)
        self.assertIsInstance(lst[0], Instruction)

    def get_instructions_by_pysh_type_invd(self):
        lst = ri.get_instructions_by_pysh_type('_foo_bar')
        self.assertEqual(lst, [])
