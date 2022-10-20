from enum import Enum
from typing import *
from dataclasses import dataclass, field
import logging

from pyshgp.push2.instruction import Instruction
from pyshgp.push2.library import INSTRUCTIONS
from pyshgp.push2.unit import Unit, Instr, Input, Block, Lit
from pyshgp.push2.state import State
import pyshgp.push2.util as u


@dataclass
class Config:
    step_limit: int = 500
    growth_limit: int = 300
    state_size_limit: int = 1e6
    number_magnitude_limit: float = 1e12
    collection_size_limit: int = 1000
    numeric_stacks: List[str] = field(default_factory=lambda: ["int", "float"])
    # @todo Add vector types to `collection_stacks`
    collection_stacks: List[str] = field(default_factory=lambda: ["str"])

    def limits(self) -> Dict[str, Callable]:
        result = {}
        for stack in self.numeric_stacks:
            result[stack] = self._constrain_number
        for stack in self.collection_stacks:
            result[stack] = self._constrain_coll
        return result

    def _constrain_number(self, n):
        return u.constrain_number(self.number_magnitude_limit, n)

    def _constrain_coll(self, coll):
        return u.constrain_collection(self.collection_size_limit, coll)


class Status(Enum):
    NORMAL = 1
    STEP_LIMIT_EXCEEDED = 2
    GROWTH_LIMIT_EXCEEDED = 3
    STATE_SIZE_LIMIT_EXCEEDED = 4


class PushException(Exception):
    def __init__(self, msg: str):
        super(PushException, self).__init__(msg)


@dataclass
class Signature:
    inputs: Dict[str, str]
    outputs: Tuple[str, ...]


@dataclass
class Program:
    signature: Signature
    code: Block
    config: Config = field(default_factory=lambda: Config())

    def __call__(self, **kwargs):
        return PushInterpreter().run(self, kwargs)


class PushInterpreter:
    def __init__(self):
        self.status = Status.NORMAL
        self._state: State = State(inputs={})

    def _eval_block(self, block: Block):
        for el in block.items[::-1]:
            self._state["exec"].push(el)

    def eval_unit(self, unit: Unit, inputs: Dict[str, str]):
        try:
            if isinstance(unit, Instr):
                INSTRUCTIONS[unit.name].evaluate(self._state)
            elif isinstance(unit, Input):
                self._state[inputs[unit.name]].push(self._state.inputs[unit.name])
            elif isinstance(unit, Block):
                self._eval_block(unit)
            elif isinstance(unit, Lit):
                self._state[unit.stack].push(unit.value)
            else:
                raise PushException(f"Cannot evaluate Push unit {unit}.")
        except Exception as e:
            raise PushException(f"Failed to eval unit {unit}.") from e

    def run(self, program: Program, inputs: Dict[str, Any]):
        self._state = State(inputs=inputs)
        # Set limits on the stacks
        for stack, limit in program.config.limits().items():
            self._state[stack].limiter = limit

        # Load the code into the exec stack.
        self._eval_block(program.code)
        logging.debug("Initial State:\n%s", self._state.pretty_str())

        steps = 0
        while len(self._state["exec"]) > 0:
            # Stopping conditions
            if steps > program.config.step_limit:
                self.status = Status.STEP_LIMIT_EXCEEDED
                break

            next_unit = self._state["exec"].pop()
            logging.debug("\nEvaluating unit: %s", next_unit)

            # Evaluate unit and enforce size/growth limits.
            old_size = self._state.size()
            self.eval_unit(next_unit, program.signature.inputs)
            new_size = self._state.size()
            if new_size > program.config.state_size_limit:
                self.status = Status.STATE_SIZE_LIMIT_EXCEEDED
                break
            elif new_size > old_size + program.config.growth_limit:
                self.status = Status.GROWTH_LIMIT_EXCEEDED
                break

            logging.debug(
                "Current state (step %s):\n%s", steps, self._state.pretty_str()
            )
            steps += 1

        return tuple(self._state.peak_stacks(program.signature.outputs))
