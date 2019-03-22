"""Concrete implementations of the Instruction Atom type."""
from typing import Callable, Set, Sequence

from pyshgp.push.state import PushState
from pyshgp.push.atoms import Instruction
from pyshgp.utils import Token


class SimpleInstruction(Instruction):
    """A simple instruction implementation.

    A SimpleInstruction uses a standardized way of manipulating PushStates. In
    other words, it handles popping its own function arguments and pushing the
    function return values.

    The first step of evaluating a SimpleInstruction is to pop the arguments
    from the stacks corresponding the instrution's ``input_types`` list.
    If multiple occurences of the same type are in ``input_types``, items are
    taken from progressively deeper in that stack. If the stacks of the
    PushState do not contain a sufficent number of items, the instruction does
    not modify the PushState.

    The popped arguments are then passed to the instruction's function to produce
    a tuple of outputs. It is crucial that the instruction's function produce a
    tuple of outputs, even if it only conains a single element. The elements of
    the tuple are then routed to the corresponding stacks specified in the
    instruction's ``output_types``.

    Parameters
    ----------
    name : str,
        A unique name for the instruction.
    f : Callable
        A function whose signature matches input_types and output_types.
    input_types : Sequence[str]
        A list of PushType names to use when popping arguments from the PushState.
    output_types : Sequence[str]
        A list of PushType names to use when pushing function results to the PushState.
    code_blocks : int
        The number of CodeBlocks to open following the instruction in a Genome.
    docstring : str, optional
        A string describing in the behavior of the Instruction.

    """

    __slots__ = ["name", "f", "input_types", "output_types", "code_blocks", "docstring"]

    def __init__(self,
                 name: str,
                 f: Callable,
                 input_types: Sequence[str],
                 output_types: Sequence[str],
                 code_blocks: int,
                 docstring="Write me!"):
        super().__init__(name, code_blocks, docstring)
        self.f = f
        self.input_types = input_types
        self.output_types = output_types

    def evaluate(self, push_state: PushState, interpreter_config):
        """Evaluate the instruction on the given PushState. Return mutated State.

        A SimpleInstruction infers which values to pop and push from the stack
        based on its `input_types` and `output_types`.

        Parameters
        ----------
        state : PushState
            Push state to modify with the Instruction.
        config : PushInterpreterConfig
            Configuration of the interpreter. Used to get various limits.

        Returns
        -------
        PushState
            Return the given state, possibly modified by the Instruction.

        """
        # Pull args, if present.
        args = push_state.observe_stacks(self.input_types)
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
        push_state.pop_from_stacks(self.input_types)
        push_state.push_to_stacks(result, self.output_types)
        return push_state

    def relevant_types(self) -> Set[str]:
        """Return a list of PushType names relevant to the instruction.

        Based on the the instructions input and output types.
        """
        return set(self.input_types + self.output_types)


class StateToStateInstruction(Instruction):
    """Instruction that takes entire PushState and returns entire PushState."""

    __slots__ = ["name", "f", "types_used", "code_blocks", "docstring"]

    def __init__(self,
                 name: str,
                 f: Callable,
                 types_used: Sequence[str],
                 code_blocks: int,
                 docstring="Write me!"):
        super().__init__(name, code_blocks, docstring)
        self.f = f
        self.types_used = set(types_used)

    def evaluate(self, push_state: PushState, interpreter_config):
        """Evaluate the instruction on the given PushState. Return mutated State.

        A SimpleInstruction infers which values to pop and push from the stack
        based on its `input_types` and `output_types`.

        Parameters
        ----------
        state : PushState
            Push state to modify with the Instruction.
        config : PushInterpreterConfig
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

    def relevant_types(self) -> Set[str]:
        """Return a list of PushType names relevant to the instruction."""
        return self.types_used


class TakesStateInstruction(Instruction):
    """Instruction that takes entire PushState and returns particular values.

    The function of a TakesStateInstruction accepts an entire PushState as input
    and produces either a ``Token.revert`` or a tuple of outputs values. It is
    crucial that the instruction's function produce a tuple of outputs, even if
    it only conains a single element.

    The elements of the tuple are then routed to the corresponding stacks
    specified in the instruction's ``output_types``.

    Additional PushTypes utilized by the instruction are denoted in ``other_types``.

    Parameters
    ----------
    name : str,
        A unique name for the instruction.
    f : Callable
        A function that takes a PushState as input and produces values corresponding to ``output_types.``
    output_types : Sequence[str]
        A list of PushType names to use when pushing function results to the PushState.
    other_types : Sequence[str]
        A list of additional PushType names used by the Insturction's function.
    code_blocks : int
        The number of CodeBlocks to open following the instruction in a Genome.
    docstring : str, optional
        A string describing in the behavior of the Instruction.

    """

    __slots__ = ["name", "f", "output_types", "other_types", "code_blocks", "docstring"]

    def __init__(self,
                 name: str,
                 f: Callable,
                 output_types: Sequence[str],
                 other_types: Sequence[str],
                 code_blocks: int,
                 docstring="Write me!"):
        super().__init__(name, code_blocks, docstring)
        self.f = f
        self.output_types = output_types
        self.other_types = other_types

    def evaluate(self, push_state: PushState, interpreter_config):
        """Evaluate the instruction on the given PushState. Return mutated State.

        A SimpleInstruction infers which values to pop and push from the stack
        based on its `input_types` and `output_types`.

        Parameters
        ----------
        state : PushState
            Push state to modify with the Instruction.
        config : PushInterpreterConfig
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
        push_state.push_to_stacks(result, self.output_types)
        return push_state

    def relevant_types(self) -> Set[str]:
        """Return a list of PushType names relevant to the instruction."""
        return set(self.other_types + self.output_types)


class ProducesManyOfTypeInstruction(Instruction):
    """Instruction that produces arbitarily many values of a given PushType.

    ProducesManyOfTypeInstructions pop their arguments in the same was as
    SimpleInstructions. Items are popped from the stacks corresponding the
    types denoted in the ``input_types`` list. If multiple occurences of the
    same type are in ``input_types``, items are taken from progressively deeper
    in that stack. If the stacks of the PushState do not contain a sufficent
    number of items, the instruction does not modify the PushState.

    The popped arguments are then passed to the instruction's function to produce
    a tuple of outputs. It is crucial that the instruction's function produce a
    tuple of outputs, even if it only conains a single element. All elements of
    the tuple are pushed individually to the stack denoted in ``output_type``.

    Parameters
    ----------
    name : str,
        A unique name for the instruction.
    f : Callable
        A function whose signature matches input_types and output_types.
    input_types : Sequence[str]
        A list of PushType names to use when popping arguments from the PushState.
    output_type : str
        The name of a PushType to use when pushing function results to the PushState.
        All values returned by the function go to the stack for this type.
    code_blocks : int
        The number of CodeBlocks to open following the instruction in a Genome.
    docstring : str, optional
        A string describing in the behavior of the Instruction.

    """

    __slots__ = ["name", "f", "input_types", "output_type", "code_blocks", "docstring"]

    def __init__(self,
                 name: str,
                 f: Callable,
                 input_types: Sequence[str],
                 output_type: str,
                 code_blocks: int,
                 docstring="Write me!"):
        super().__init__(name, code_blocks, docstring)
        self.f = f
        self.input_types = input_types
        self.output_type = output_type

    def evaluate(self, push_state: PushState, interpreter_config):
        """Evaluate the instruction on the given PushState. Return mutated State.

        A ProducesManyOfTypeInstruction infers which values to pop from the stack
        based on `input_types` and pushes each output to the same stack
        based on `output_type`.

        Parameters
        ----------
        state : PushState
            Push state to modify with the Instruction.
        config : PushInterpreterConfig
            Configuration of the interpreter. Used to get various limits.

        Returns
        -------
        PushState
            Return the given state, possibly modified by the Instruction.

        """
        # Pull args, if present.
        args = push_state.observe_stacks(self.input_types)
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
        push_state.pop_from_stacks(self.input_types)
        push_state.push_to_stacks(result, [self.output_type] * len(result))
        return push_state

    def relevant_types(self) -> Set[str]:
        """Return a list of PushType names relevant to the instruction.

        Based on the the instructions input types and output type.
        """
        return set(self.input_types + [self.output_type])
