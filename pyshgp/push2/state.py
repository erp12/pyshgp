from enum import Enum
from typing import *

from pyshgp.push2.util import Token


def _identity(x):
    return x


E = TypeVar("E")


class Stack(Generic[E]):
    __slots__ = ["items", "limiter"]

    def __init__(
        self, *,
        items: Sequence[E] = None,
        limiter: Callable[[Any], E] = None
    ):
        self.items = []
        if items is not None:
            self.items = list(items)

        self.limiter = limiter
        if limiter is None:
            self.limiter = _identity

    def push(self, item: E):
        self.items.append(self.limiter(item))

    def push_all(self, lst: List[E]):
        self.items = self.items + lst[::-1]

    def pop(self, idx: int = 0) -> E:
        if len(self.items) <= idx:
            return Token.NO_ITEM
        return self.items.pop(self._underlying_idx(idx))

    def pop_n(self, n: int) -> List[E]:
        popped = self.items[-n:]
        self.items = self.items[:-n]
        return popped

    def peak(self, idx: int = 0) -> E:
        if len(self.items) <= idx:
            return Token.NO_ITEM
        return self.items[self._underlying_idx(idx)]

    def insert(self, idx: int, item: E):
        self.items.insert(self._underlying_idx(idx), item)

    def __len__(self) -> int:
        return len(self.items)

    def _underlying_idx(self, idx: int) -> int:
        return len(self.items) - idx - 1

    def __repr__(self):
        items_str = self.items[::-1].__repr__().strip("[]")
        return f"Stack({items_str})"


class ReservedStacks(Enum):
    STDOUT = "stdout"


RESERVED_STACKS = set([e.value for e in ReservedStacks])


class State(Dict[str, Stack]):
    __slots__ = ["stdout", "inputs"]

    def __init__(self, *, inputs: Dict[str, Any] = None):
        super(State, self).__init__()
        self.stdout = ""
        self.inputs = inputs
        if inputs is None:
            self.inputs = {}

    def peak_stacks(self, stacks: Sequence[str]) -> List:
        values = []
        counts = {}
        for stack in stacks:
            if stack == "stdout":
                values.append(self.stdout)
            else:
                ndx = counts.get(stack, 0)
                from_stack = self[stack].peak(ndx)
                if from_stack == Token.NO_ITEM:
                    return from_stack
                values.append(from_stack)
                counts[stack] = ndx + 1
        return values

    def pop_stacks(self, stacks: Sequence[str]) -> Union[List, Token]:
        # First check that enough items exist on stacks.
        for stack, num_needed in Counter(stacks):
            if len(self[stack]) < num_needed:
                return Token.NO_ITEM
        # Pop stacks.
        values = []
        for stack in stacks:
            values.append(self[stack].pop())
        return values

    def push_stacks(self, values: Sequence[Any], stacks: Sequence[str]):
        for idx in range(len(values)):
            stack = stacks[idx]
            if stack == ReservedStacks.STDOUT.value:
                self.stdout += str(values[idx])
            else:
                self[stack].push(values[idx])

    def size(self) -> int:
        return sum([len(stack) for stack in self.values()])

    def pretty_str(self):
        lines = []
        for k, v in self.items():
            lines.append(f"{k}:\t{v}")
        lines.append(f"inputs:\t{self.inputs}")
        lines.append(f"stdout:\t{self.stdout}")
        return "\n".join(lines)

    def add_stack(self, name: str, items: Sequence[E] = None, limiter: Callable[[Any], E] = None):
        if name in RESERVED_STACKS:
            raise ValueError(
                f"Cannot create Push stack under reserved name '{name}'."
            )
        self[name] = Stack(items=items, limiter=limiter)

    def __getitem__(self, stack: str) -> Stack:
        if stack not in self:
            self.add_stack(stack)
        return super(State, self).__getitem__(stack)

    def __eq__(self, other) -> bool:
        if not isinstance(other, State):
            return False
        return (
                super(State).__eq__(other)
                and self.inputs == other.inputs
                and self.stdout == other.stdout
        )
