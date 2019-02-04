import pytest

from pyshgp.push.instruction_set import InstructionSet, _CORE_INSTRUCTIONS
from pyshgp.push.types import PushType


class TestInstructionSet:

    def test_register(self, atoms):
        i_set = InstructionSet()
        i_set.register(atoms["add"])
        assert len(i_set) == 1

    def test_register_list(self, atoms):
        i_set = InstructionSet()
        i_set.register_list([atoms["add"], atoms["sub"]])
        assert len(i_set) == 2

    def test_register_by_type(self):
        i_set = InstructionSet()
        i_set.register_by_type(["int"])
        for i in i_set.values():
            assert "int" in i.relevant_types()

    def test_register_by_name(self):
        i_set = InstructionSet()
        i_set.register_by_name(".*_mult")
        print(i_set)
        assert len(i_set) == 2
        assert set([i.name for i in i_set.values()]) == {"int_mult", "float_mult"}

    def test_register_all(self):
        i_set = InstructionSet().register_all()
        # assert len(i_set) == len(_CORE_INSTRUCTIONS)  # If fail, likely duplicated instr names.
        assert set(i_set.values()) == set(_CORE_INSTRUCTIONS)

    def test_unregister(self, atoms):
        i_set = InstructionSet()
        i_set.register(atoms["add"])
        i_set.register(atoms["sub"])
        i_set.unregister("int_add")
        assert len(i_set) == 1
        assert list(i_set.values())[0].name == "int_sub"

    def test_supported_types(self, instr_set):
        type_names = set([t.name if isinstance(t, PushType) else t for t in instr_set.supported_types()])
        assert type_names == {"code", "int", "float", "bool", "str", "exec", "char", "stdout"}
