import pytest

from pyshgp.push.stack import PushStack
from pyshgp.push.types import PushInt, PushStr
from pyshgp.utils import Token
from pyshgp.validation import PushError


@pytest.fixture(scope="function")
def int_stack(atoms, push_config):
    return PushStack(PushInt, push_config)


@pytest.fixture(scope="function")
def str_stack(atoms, push_config):
    return PushStack(PushStr, push_config)


class TestPushStack:

    def test_push(self, int_stack: PushStack):
        int_stack.push(5)
        assert len(int_stack) == 1

    def test_push_wrong_type(self, int_stack: PushStack):
        with pytest.raises(PushError):
            int_stack.push("zz")

    def test_nth(self, int_stack: PushStack):
        int_stack.push(5).push(4).push(3)
        assert int_stack.nth(1) == 4

    def test_nth_oob(self, int_stack: PushStack):
        int_stack.push(5)
        assert int_stack.nth(1) == Token.no_stack_item

    def test_top(self, int_stack: PushStack):
        int_stack.push(5).push(-10)
        assert int_stack.top() == -10

    def test_top_of_empty(self, int_stack: PushStack):
        assert int_stack.top() == Token.no_stack_item

    def test_insert(self, str_stack: PushStack):
        str_stack.push("a").push("b").push("c").insert(1, "z")
        assert len(str_stack) == 4
        assert str_stack.nth(1) == "z"
        assert str_stack.nth(2) == "b"

    def test_insert_oob(self, str_stack: PushStack):
        str_stack.push("a").push("b").push("c").insert(10, "z")
        assert len(str_stack) == 4
        assert str_stack.nth(1) == "b"
        assert str_stack.nth(3) == "z"

    def test_set_nth(self, str_stack: PushStack):
        str_stack.push("a").push("b").push("c").push("d").set_nth(1, "z")
        assert len(str_stack) == 4
        assert str_stack.nth(1) == "z"

    def test_set_nth_oob(self, str_stack: PushStack):
        with pytest.raises(IndexError):
            str_stack.push("a").push("b").push("c").set_nth(10, "z")

    def test_flush(self, int_stack: PushStack):
        int_stack.push(1).push(-1).flush()
        assert len(int_stack) == 0

    def test_large_str(self, str_stack: PushStack):
        s = "largestr"*1000
        str_stack.push(s)
        assert len(str_stack.pop()) != len(s)
