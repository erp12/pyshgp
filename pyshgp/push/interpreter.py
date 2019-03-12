"""The :mod:`interpreter` module defines the ``PushInterpreter`` class.

A ``PushInterpreter`` is capable of running Push programs and returning their
output. Push interpreters can be configured with a ``PushInterpreterConfig``
class to determine limits.
"""

from typing import Sequence, Union
import time
from enum import Enum

from pyshgp.push.state import PushState
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.atoms import (
    Atom, Closer, Literal, Instruction, JitInstructionRef, CodeBlock
)
from pyshgp.validation import PushError
from pyshgp.monitoring import VerbosityConfig, DEFAULT_VERBOSITY_LEVELS


class PushInterpreterConfig:
    """Define a configuration for PushInterpreter.

    Parameters
    ----------
    atom_limit : int, optional
        Max number of atoms to process before terminating the execution of a
        given program. Default is 500
    growth_cap : int, optional
        Max number of elements that can be added to a PushState at any given
        step of program execution. If exceeded, program terminates. Default is
        500.
    runtime_limit : int, optional
        Max number of milliseconds to run a push program before forcing
        termination. Default is 2e10.
    reset_on_run : bool, optional
        If True, interpreter's state and status are reset every time a program
        is run. Default is True.


    Attributes
    ----------
    atom_limit : int
        Max number of atoms to process before terminating the execution of a
        given program. Default is 500
    growth_cap : int
        Max number of elements that can be added to a PushState at any given
        step of program execution. If exceeded, program terminates. Default is
        500.
    runtime_limit : int
        Max number of milliseconds to run a push program before forcing
        termination. Default is 2e10.
    reset_on_run : bool
        If True, interpreter's state and status are reset every time a program
        is run. Default is True.

    """

    # @TODO: Should PushInterpreterConfig be JSON serializable?
    # @TODO: Refactor atom_limit to step_limit

    def __init__(self, *,
                 atom_limit=500,
                 growth_cap=500,
                 runtime_limit=2e10,
                 reset_on_run=True):
        self.atom_limit = atom_limit
        self.growth_cap = growth_cap
        self.runtime_limit = runtime_limit
        self.reset_on_run = reset_on_run


class PushInterpreterStatus(Enum):
    """Enum class of all potential statuses of a PushInterpreter."""

    normal = 1
    atom_limit_exceeded = 2
    runtime_limit_exceeded = 3
    growth_cap_exceeded = 4


class PushInterpreter:
    """An interpreter capable of running Push programs.

    Parameters
    ----------
    instruction_set : Union[InstructionSet, str], optional
        The InstructionSet to use for executing programs. Default is "core"
        which instansiates an InstructionSet using all the core instructions.
    config : PushInterpreterConfig, optional
        A PushInterpreterConfig specifying limits and early termination
        conditions. Default is None, which creates a config will all default
        values.

    Attributes
    ----------
    instruction_set : InstructionSet
        The InstructionSet to use for executing programs.
    config : PushInterpreterConfig
        A PushInterpreterConfig specifying limits and early termination
        conditions.
    state : PushState
        The current PushState. Contains one stack for each PushType utilized
        mentioned by the instructions in the instruction set.
    status : PushInterpreterStatus
        A string denoting if the Interpreter has enountered a situation
        where non-standard termination was required.

    """

    def __init__(self,
                 instruction_set: Union[InstructionSet, str] = "core",
                 config: PushInterpreterConfig = None):
        # If no instruction set given, create one and register all instructions.
        if instruction_set == "core":
            self.instruction_set = InstructionSet(register_all=True)
        else:
            self.instruction_set = instruction_set
        self._supported_types = self.instruction_set.supported_types()

        if config is None:
            self.config = PushInterpreterConfig()
        else:
            self.config = config

        # Initialize the PushState and status
        self.reset()

    def reset(self):
        """Reset the interpreter status and PushState."""
        self.state = PushState(self._supported_types)
        self.status = PushInterpreterStatus.normal

    def _evaluate_instruction(self, instruction: Union[Instruction, JitInstructionRef]):
        self.state = instruction.evaluate(self.state, self.config)

    def evaluate_atom(self, atom: Atom):
        """Evaluate an Atom.

        Parameters
        ----------
        atom : Atom
            The Atom (Literal, Instruction, JitInstructionRef, or CodeBlock) to
            evaluate against the current PushState.

        """
        try:
            if isinstance(atom, Instruction):
                self._evaluate_instruction(atom)
            elif isinstance(atom, JitInstructionRef):
                self._evaluate_instruction(self.instruction_set[atom.name])
            elif isinstance(atom, CodeBlock):
                for a in atom[::-1]:
                    self.state["exec"].push(a)
            elif isinstance(atom, Literal):
                self.state[atom.push_type.name].push(atom.value)
            elif isinstance(atom, Closer):
                raise PushError("Closers should not be in push programs. Only genomes.")
            else:
                raise PushError("Cannont evaluate {t}, require a subclass of Atom".format(t=type(atom)))
        except Exception as e:
            err_type = type(e).__name__
            err_msg = str(e)
            raise PushError(
                "{t} raised while evaluating {atom}. Origional mesage: \"{m}\"".format(
                    t=err_type,
                    atom=atom,
                    m=err_msg
                )
            )

    def run(self,
            program: CodeBlock,
            inputs: Sequence,
            output_types: Sequence[str],
            verbosity_config: VerbosityConfig = None):
        """Run a Push program given some inputs and desired output PushTypes.

        The general flow of this method is:
            1. Create a new push state
            2. Load the program and inputs.
            3. If the exec stack is empty, return the outputs.
            4. Else, pop the exec stack and process the atom.
            5. Return to step 3.

        Parameters
        ----------
        program
            Program to run.
        inputs
            A sequence of values to use as inputs to the push program.
        output_types
            A secence of values that denote the Pushtypes of the expected
            outputs of the push program.
        verbosity_config : VerbosityConfig, optional
            A VerbosityConfig controling what is logged during the execution
            of the program. Default is no verbosity.

        Returns
        -------
        Sequence
            A sequence of values pulled from the final push state. May contain
            pyshgp.utils.Token.no_stack_item if needed stacks are empty.

        """
        if self.config.reset_on_run:
            self.reset()

        self.state.load_program(program)
        self.state.load_inputs(inputs)
        stop_time = time.time() + self.config.runtime_limit
        steps = 0

        if verbosity_config is None:
            verbosity_config = DEFAULT_VERBOSITY_LEVELS[0]
        verbose_trace = verbosity_config.program_trace

        if verbose_trace:
            verbose_trace("Initial State:")
            self.state.pretty_print(verbose_trace)

        while len(self.state["exec"]) > 0:
            if steps > self.config.atom_limit:
                self.status = PushInterpreterStatus.atom_limit_exceeded
                break
            if time.time() > stop_time:
                self.status = PushInterpreterStatus.runtime_limit_exceeded
                break

            next_atom = self.state["exec"].pop()

            if verbose_trace:
                verbose_trace("Current Atom: " + str(next_atom))

            old_size = len(self.state)
            self.evaluate_atom(next_atom)
            if len(self.state) > old_size + self.config.growth_cap:
                self.status = PushInterpreterStatus.growth_cap_exceeded
                break

            if verbose_trace:
                verbose_trace("Current State:")
                self.state.pretty_print(verbose_trace)
            steps += 1

        if verbose_trace:
            verbose_trace("Finished program evaluation.")

        return self.state.observe_stacks(output_types)


DEFAULT_INTERPRETER = PushInterpreter()
