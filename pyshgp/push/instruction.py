"""Concrete implementations of the Instruction Atom type."""
from abc import ABC, abstractmethod
from typing import Callable, Set, Sequence

from pyshgp.push.atoms import InstructionMeta
from pyshgp.push.config import PushConfig
from pyshgp.push.type_library import RESERVED_PSEUDO_STACKS
from pyshgp.push.state import PushState
from pyshgp.utils import Token


class Instruction(ABC):
    """A function in the Push language used to modify the PushState.

    The Instruction class is the abstract base class for specific implementations
    that are configured differently. For example, see SimpleInstruction verses
    TakesStateInstruction.

    Parameters
    ----------
    name : str,
        A unique name for the instruction.
    code_blocks : int
        The number of CodeBlocks to open following the instruction in a Genome.
    docstring : str, optional
        A string describing in the behavior of the Instruction.

    Attributes
    ----------
    name : str,
        A unique name for the instruction.
    code_blocks : int
        The number of CodeBlocks to open following the instruction in a Genome.
    docstring : str, optional
        A string describing in the behavior of the Instruction.

    """

    __slots__ = ["name", "code_block", "docstring"]

    def __init__(self, name: str, code_blocks: int, docstring="Write me!"):
        self.name = name
        self.code_blocks = code_blocks
        self.docstring = docstring

    @abstractmethod
    def evaluate(self, push_state: PushState, push_config: PushConfig = None) -> PushState:
        """Evaluate the instruction on the given PushState.

        Parameters
        ----------
        push_state: pyshgp.push.state.PushState
            The PushState to run the instruction on.
        push_config: pyshgp.push.interpreter.PushConfig
            The configuration of the Push language.

        Returns
        -------
        pyshgp.push.state.PushState
            Return the given state, possibly modified by the Instruction.

        """
        pass

    @abstractmethod
    def required_stacks(self) -> Set[str]:
        """Return a list of PushType names relevant to the instruction."""
        pass

    def meta(self) -> InstructionMeta:
        """Create an ``InstructionMeta`` from the instruction object."""
        return InstructionMeta(name=self.name, code_blocks=self.code_blocks)

    def __eq__(self, other):
        if type(self) == type(other):
            return self.name == other.name
        return False

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        return "Instruction<{n}>".format(n=self.name)


class SimpleInstruction(Instruction):
    """A simple instruction implementation.

    A SimpleInstruction uses a standardized way of manipulating PushStates. In
    other words, it handles popping its own function arguments and pushing the
    function return values.

    The first step of evaluating a SimpleInstruction is to pop the arguments
    from the stacks corresponding the instruction's ``input_stacks`` list.
    If multiple occurrences of the same type are in ``input_stacks``, items are
    taken from progressively deeper in that stack. If the stacks of the
    PushState do not contain a sufficient number of items, the instruction does
    not modify the PushState.

    The popped arguments are then passed to the instruction's function to produce
    a tuple of outputs. It is crucial that the instruction's function produce a
    tuple of outputs, even if it only contains a single element. The elements of
    the tuple are then routed to the corresponding stacks specified in the
    instruction's ``output_stacks``.

    Parameters
    ----------
    name : str,
        A unique name for the instruction.
    f : Callable
        A function whose signature matches input_stacks and output_stacks.
    input_stacks : Sequence[str]
        A list of PushType names to use when popping arguments from the PushState.
    output_stacks : Sequence[str]
        A list of PushType names to use when pushing function results to the PushState.
    code_blocks : int
        The number of CodeBlocks to open following the instruction in a Genome.
    docstring : str, optional
        A string describing in the behavior of the Instruction.

    """

    __slots__ = ["name", "f", "input_stacks", "output_stacks", "code_blocks", "docstring"]

    def __init__(self,
                 name: str,
                 f: Callable,
                 input_stacks: Sequence[str],
                 output_stacks: Sequence[str],
                 code_blocks: int,
                 docstring="Write me!"):
        super().__init__(name, code_blocks, docstring)
        self.f = f
        self.input_stacks = input_stacks
        self.output_stacks = output_stacks

    def evaluate(self, push_state: PushState, push_config: PushConfig = None) -> PushState:
        """Evaluate the instruction on the given PushState. Return mutated State.

        A SimpleInstruction infers which values to pop and push from the stack
        based on its `input_stacks` and `output_stacks`.

        Parameters
        ----------
        push_state : PushState
            Push state to modify with the Instruction.
        push_config :  pyshgp.push.interpreter.PushConfig
            Configuration of the interpreter. Used to get various limits.

        Returns
        -------
        PushState
            Return the given state, possibly modified by the Instruction.

        """
        # Pull args, if present.
        args = push_state.observe_stacks(self.input_stacks)
        if Token.no_stack_item in args:
            return push_state

        # Compute result, return if revert or response too big.
        result = self.f(*args)
        if result is Token.revert:
            return push_state
        if not isinstance(result, (list, tuple)):
            raise ValueError("Instruction result must be a collection. {i} gave {t}.".format(
                i=self,
                t=type(result)
            ))

        # Remove arguments, push results.
        push_state.pop_from_stacks(self.input_stacks)
        push_state.push_to_stacks(result, self.output_stacks)
        return push_state

    def required_stacks(self) -> Set[str]:
        """Return a list of PushType names relevant to the instruction.

        Based on the the instructions input and output types.
        """
        return set(self.input_stacks + self.output_stacks) - RESERVED_PSEUDO_STACKS


class StateToStateInstruction(Instruction):
    """Instruction that takes entire PushState and returns entire PushState."""

    __slots__ = ["name", "f", "stacks_used", "code_blocks", "docstring"]

    def __init__(self,
                 name: str,
                 f: Callable,
                 stacks_used: Sequence[str],
                 code_blocks: int,
                 docstring="Write me!"):
        super().__init__(name, code_blocks, docstring)
        self.f = f
        self.stacks_used = set(stacks_used)

    def evaluate(self, push_state: PushState, push_config: PushConfig = None) -> PushState:
        """Evaluate the instruction on the given PushState. Return mutated State.

        A SimpleInstruction infers which values to pop and push from the stack
        based on its `input_stacks` and `output_stacks`.

        Parameters
        ----------
        push_state : PushState
            Push state to modify with the Instruction.
        push_config : PushConfig
            Configuration of the interpreter. Used to get various limits.

        Returns
        -------
        PushState
            Return the given state, possibly modified by the Instruction.

        """
        result = self.f(push_state)
        if result == Token.revert:
            return push_state
        else:
            return result

    def required_stacks(self) -> Set[str]:
        """Return a list of PushType names relevant to the instruction."""
        return self.stacks_used - RESERVED_PSEUDO_STACKS


class TakesStateInstruction(Instruction):
    """Instruction that takes entire PushState and returns particular values.

    The function of a TakesStateInstruction accepts an entire PushState as input
    and produces either a ``Token.revert`` or a tuple of outputs values. It is
    crucial that the instruction's function produce a tuple of outputs, even if
    it only conains a single element.

    The elements of the tuple are then routed to the corresponding stacks
    specified in the instruction's ``output_stacks``.

    Additional PushTypes utilized by the instruction are denoted in ``other_stacks``.

    Parameters
    ----------
    name : str,
        A unique name for the instruction.
    f : Callable
        A function that takes a PushState as input and produces values corresponding to ``output_stacks.``
    output_stacks : Sequence[str]
        A list of PushType names to use when pushing function results to the PushState.
    other_stacks : Sequence[str]
        A list of additional PushType names used by the Insturction's function.
    code_blocks : int
        The number of CodeBlocks to open following the instruction in a Genome.
    docstring : str, optional
        A string describing in the behavior of the Instruction.

    """

    __slots__ = ["name", "f", "output_stacks", "other_stacks", "code_blocks", "docstring"]

    def __init__(self,
                 name: str,
                 f: Callable,
                 output_stacks: Sequence[str],
                 other_stacks: Sequence[str],
                 code_blocks: int,
                 docstring="Write me!"):
        super().__init__(name, code_blocks, docstring)
        self.f = f
        self.output_stacks = output_stacks
        self.other_stacks = other_stacks

    def evaluate(self, push_state: PushState, push_config: PushConfig = None) -> PushState:
        """Evaluate the instruction on the given PushState. Return mutated State.

        A SimpleInstruction infers which values to pop and push from the stack
        based on its `input_stacks` and `output_stacks`.

        Parameters
        ----------
        push_state : PushState
            Push state to modify with the Instruction.
        push_config : PushConfig
            Configuration of the interpreter. Used to get various limits.

        Returns
        -------
        PushState
            Return the given state, possibly modified by the Instruction.

        """
        # Compute result. State should be modified in place during function.
        result = self.f(push_state)

        # Return if revert.
        if result is Token.revert:
            return push_state
        if not isinstance(result, (list, tuple)):
            raise ValueError("Instruction result must be a collection. {i} gave {t}.".format(
                i=self,
                t=type(result)
            ))

        # Push results.
        push_state.push_to_stacks(result, self.output_stacks)
        return push_state

    def required_stacks(self) -> Set[str]:
        """Return a list of PushType names relevant to the instruction."""
        return set(self.other_stacks + self.output_stacks) - RESERVED_PSEUDO_STACKS


class ProducesManyOfTypeInstruction(Instruction):
    """Instruction that produces arbitarily many values of a given PushType.

    ProducesManyOfTypeInstructions pop their arguments in the same was as
    SimpleInstructions. Items are popped from the stacks corresponding the
    types denoted in the ``input_stacks`` list. If multiple occurences of the
    same type are in ``input_stacks``, items are taken from progressively deeper
    in that stack. If the stacks of the PushState do not contain a sufficent
    number of items, the instruction does not modify the PushState.

    The popped arguments are then passed to the instruction's function to produce
    a tuple of outputs. It is crucial that the instruction's function produce a
    tuple of outputs, even if it only conains a single element. All elements of
    the tuple are pushed individually to the stack denoted in ``output_stack``.

    Parameters
    ----------
    name : str,
        A unique name for the instruction.
    f : Callable
        A function whose signature matches input_stacks and output_stacks.
    input_stacks : Sequence[str]
        A list of PushType names to use when popping arguments from the PushState.
    output_stack : str
        The name of a PushType to use when pushing function results to the PushState.
        All values returned by the function go to the stack for this type.
    code_blocks : int
        The number of CodeBlocks to open following the instruction in a Genome.
    docstring : str, optional
        A string describing in the behavior of the Instruction.

    """

    __slots__ = ["name", "f", "input_stacks", "output_stack", "code_blocks", "docstring"]

    def __init__(self,
                 name: str,
                 f: Callable,
                 input_stacks: Sequence[str],
                 output_stack: str,
                 code_blocks: int,
                 docstring="Write me!"):
        super().__init__(name, code_blocks, docstring)
        self.f = f
        self.input_stacks = input_stacks
        self.output_stack = output_stack

    def evaluate(self, push_state: PushState, push_config: PushConfig = None) -> PushState:
        """Evaluate the instruction on the given PushState. Return mutated State.

        A ProducesManyOfTypeInstruction infers which values to pop from the stack
        based on `input_stacks` and pushes each output to the same stack
        based on `output_stack`.

        Parameters
        ----------
        push_state : PushState
            Push state to modify with the Instruction.
        push_config : PushConfig
            Configuration of the interpreter. Used to get various limits.

        Returns
        -------
        PushState
            Return the given state, possibly modified by the Instruction.

        """
        # Pull args, if present.
        args = push_state.observe_stacks(self.input_stacks)
        if Token.no_stack_item in args:
            return push_state

        # Compute result, return if revert or response too big.
        result = self.f(*args)
        if result is Token.revert:
            return push_state
        if not isinstance(result, (list, tuple)):
            raise ValueError("Instruction result must be a collection. {i} gave {t}.".format(
                i=self,
                t=type(result)
            ))

        # Remove arguments, push results.
        push_state.pop_from_stacks(self.input_stacks)
        push_state.push_to_stacks(result, [self.output_stack] * len(result))
        return push_state

    def required_stacks(self) -> Set[str]:
        """Return a list of PushType names relevant to the instruction.

        Based on the the instructions input types and output type.
        """
        return set(self.input_stacks + [self.output_stack]) - RESERVED_PSEUDO_STACKS
