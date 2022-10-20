from copy import deepcopy

import pytest

from push2.state import State
from pyshgp.push2.instruction import SimpleInstruction, InstructionMeta, Item, Stack


@pytest.fixture
def item_to_item():
    return SimpleInstruction(
        meta=InstructionMeta("item_to_item"),
        fn=lambda x, y: x + y,
        inputs=(Item("A"), Item("B")),
        outputs=(Item("C"),),
        invariants=[lambda x, y: x != y],
    )


@pytest.fixture
def stack_to_item():
    return SimpleInstruction(
        meta=InstructionMeta("stack_to_item"),
        fn=lambda a: len(a),
        inputs=(Stack("A"),),
        outputs=(Item("B"),),
    )


@pytest.fixture
def stack_to_stack():
    return SimpleInstruction(
        meta=InstructionMeta("stack_to_stack"),
        fn=lambda a: a[::-1],
        inputs=(Stack("A"),),
        outputs=(Stack("B"),),
    )


class TestSimpleInstruction:
    def test_uses_stacks(
        self,
        item_to_item: SimpleInstruction,
        stack_to_item: SimpleInstruction,
        stack_to_stack: SimpleInstruction,
    ):
        assert item_to_item.uses_stacks() == {"A", "B", "C"}
        assert stack_to_item.uses_stacks() == {"A", "B"}
        assert stack_to_stack.uses_stacks() == {"A", "B"}

    def test_item_to_item(self, item_to_item):
        state = State()
        state.push_stacks([1, 2], ["A", "B"])
        expected = State()
        expected.add_stack("A")
        expected.add_stack("B")
        expected["C"].push(3)
        item_to_item.evaluate(state)
        assert state == expected

    def test_stack_to_item(self, stack_to_item):
        state = State()
        state.push_stacks([1, 2, 3], ["A", "A", "A"])
        expected = State()
        expected.add_stack("A")
        expected["B"].push(3)
        stack_to_item.evaluate(state)
        assert state == expected

    def test_stack_to_stack(self, stack_to_stack):
        state = State()
        state.push_stacks([1, 2, 3], ["A", "A", "A"])
        expected = State()
        expected.add_stack("A")
        expected["B"].push_all([3, 2, 1])
        stack_to_stack.evaluate(state)
        assert state == expected

    def test_insufficient_args(self, item_to_item):
        state = State()
        state.push_stacks([1], ["A"])
        expected = deepcopy(state)
        item_to_item.evaluate(state)
        assert state == expected

    def test_invariants(self, item_to_item):
        state = State()
        state.push_stacks([1, 1], ["A", "B"])
        expected = deepcopy(state)
        item_to_item.evaluate(state)
        assert state == expected
