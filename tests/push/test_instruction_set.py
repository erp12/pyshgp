import pytest
from itertools import chain

from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.instructions import common, numeric, text, code, io, logical, vector


@pytest.fixture(scope="function")
def all_core_instructions(core_type_lib):
    return set(chain(
        common.instructions(core_type_lib),
        io.instructions(core_type_lib),
        code.instructions(core_type_lib),
        numeric.instructions(core_type_lib),
        text.instructions(core_type_lib),
        logical.instructions(core_type_lib),
        vector.instructions(core_type_lib),
    ))


class TestInstructionSet:

    def test_register(self, instr_set):
        i_set = InstructionSet()
        i_set.register(instr_set["int_add"])
        assert len(i_set) == 1

    def test_register_list(self, instr_set):
        i_set = InstructionSet()
        i_set.register_list([instr_set["int_add"], instr_set["int_sub"]])
        assert len(i_set) == 2

    def test_register_core_by_stack(self):
        i_set = InstructionSet()
        i_set.register_core_by_stack({"int"})
        for i in i_set.values():
            if len(i.required_stacks()) > 0:
                assert "int" in i.required_stacks()

    def test_register_core_by_stack_with_exclude(self, core_type_lib):
        foo = common.instructions(core_type_lib)
        print([i for i in foo if i.name == "exec_dup_times"][0].required_stacks())

        i_set = InstructionSet(register_core=False)
        i_set.register_core_by_stack({"int"}, exclude_stacks={"str", "exec", "code"})
        for i in i_set.values():
            if len(i.required_stacks()) > 0:
                print(i.name, i.required_stacks())
                assert i.name not in {"exec_pop",
                                      "exec_dup",
                                      "exec_dup_times",
                                      "exec_swap",
                                      "exec_rot",
                                      "exec_flush",
                                      "exec_stack_depth",
                                      "exec_yank",
                                      "exec_yank_dup",
                                      "exec_shove",
                                      "exec_shove_dup"}
                assert "int" in i.required_stacks()
                assert "exec" not in i.required_stacks()

    def test_register_core_by_name(self):
        i_set = InstructionSet()
        i_set.register_core_by_name(".*_mult")
        assert len(i_set) == 2
        assert set([i.name for i in i_set.values()]) == {"int_mult", "float_mult"}

    def test_register_core(self, all_core_instructions):
        i_set = InstructionSet().register_core()
        assert set(i_set.values()) == all_core_instructions

    def test_unregister(self, instr_set):
        i_set = InstructionSet()
        i_set.register(instr_set["int_add"])
        i_set.register(instr_set["int_sub"])
        i_set.unregister("int_add")
        assert len(i_set) == 1
        assert list(i_set.values())[0].name == "int_sub"

    def test_required_stacks(self, instr_set):
        assert instr_set.required_stacks() == {
            "exec", "code", "int", "float", "bool", "str", "char",
            'vector_str', 'vector_char', 'vector_bool', 'vector_int', 'vector_float'
        }


# @TODO: TEST - Test all instruction set methods with custom type library.
