from pyshgp.push.atoms import AtomFactory, Closer
from pyshgp.push.types import PushInt


class TestAtomFactory:

    def test_decode_close(self, instr_set):
        atom = AtomFactory.json_dict_to_atom({"a": "close"}, instr_set)
        assert atom == Closer()

    def test_decode_lit(self, instr_set):
        atom = AtomFactory.json_dict_to_atom({"a": "lit", "t": "int", "v": 17}, instr_set)
        assert atom.value == 17
        assert atom.push_type == PushInt

    def test_decode_lit(self, instr_set, atoms):
        atom = AtomFactory.json_dict_to_atom({"a": "instr", "n": "int_add"}, instr_set)
        assert atom == atoms["add"]
