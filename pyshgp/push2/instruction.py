from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import *

from pyshgp.push2.state import State
from pyshgp.push2.util import Token


class StackRef:
    def __init__(self, stack: str):
        self.stack = stack


@dataclass
class Item(StackRef):
    stack: str


@dataclass
class Stack(StackRef):
    stack: str
    min_size: int = 0


@dataclass
class InstructionMeta:
    name: str
    blocks: int = None
    docstring: str = field(default=None, repr=False)


class Instruction(ABC):
    __slots__ = ["meta"]

    def __init__(self, meta: InstructionMeta):
        self.meta = meta

    @abstractmethod
    def evaluate(self, state: State) -> None:
        pass

    @abstractmethod
    def uses_stacks(self) -> Set[str]:
        pass


class SimpleInstruction(Instruction):
    __slots__ = ["meta", "fn", "inputs", "outputs", "invariants"]

    def __init__(
        self,
        meta: InstructionMeta,
        fn: Callable,
        inputs: Tuple[StackRef, ...],
        outputs: Tuple[StackRef, ...],
        invariants: Sequence[Callable[[Any, ...], bool]] = None,
    ):
        super(SimpleInstruction, self).__init__(meta)
        self.fn = fn
        self.inputs = inputs
        self.outputs = outputs
        self.invariants = invariants
        if self.invariants is None:
            self.invariants = []

    def evaluate(self, state: State) -> None:
        # Peak args in order
        args = []
        depths: Dict[str, int] = {}
        for i in self.inputs:
            if isinstance(i, Item):
                depth = depths.get(i.stack, 0)
                args.append(state[i.stack].peak(depth))
                depths[i.stack] = depth + 1
            elif isinstance(i, Stack):
                stack = state[i.stack]
                if len(stack) >= i.min_size:
                    args.append(stack.items)
                else:
                    args.append(Token.NO_ITEM)
            else:
                raise RuntimeError("unreachable")

        # Return early on missing args
        if Token.NO_ITEM in args:
            return

        # Return early on violated invariants
        for pred in self.invariants:
            if not pred(*args):
                return

        # Run function, ensure output is tuple
        result = self.fn(*args)
        if result == Token.NOOP:
            return
        if len(self.outputs) == 1 and not isinstance(result, tuple):
            result = (result,)

        # Pop args items
        for stack, depth in depths.items():
            state[stack].pop_n(depth)

        # Push results.
        for out_ref, out_val in zip(self.outputs, result):
            if isinstance(out_ref, Item):
                state[out_ref.stack].push(out_val)
            elif isinstance(out_ref, Item):
                state[out_ref.stack].push_all(out_val)

    def uses_stacks(self) -> Set[str]:
        return set([s.stack for s in (self.inputs + self.outputs)])
