"""The :mod:`interpreter` module defines the ``PushInterpreter`` class.

A ``PushInterpreter`` is capable of running Push programs and returning their
output. Push interpreters can be configured with a ``PushInterpreterConfig``
class to determine limits.
"""

from typing import Sequence, Union
import time
from enum import Enum

from pyshgp.push.program import Program
from pyshgp.push.state import PushState
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.atoms import Atom, Closer, Literal, Instruction, JitInstructionRef, CodeBlock
from pyshgp.push.types import PushStr
from pyshgp.push.config import PushConfig
from pyshgp.validation import PushError
from pyshgp.monitoring import VerbosityConfig, DEFAULT_VERBOSITY_LEVELS, log_function


class PushInterpreterStatus(Enum):
    """Enum class of all potential statuses of a PushInterpreter."""

    normal = 1
    step_limit_exceeded = 2
    runtime_limit_exceeded = 3
    growth_cap_exceeded = 4


class PushInterpreter:
    """An interpreter capable of running Push programs.

    Parameters
    ----------
    instruction_set : Union[InstructionSet, str], optional
        The InstructionSet to use for executing programs. Default is "core"
        which instansiates an InstructionSet using all the core instructions.
    verbosity_config : VerbosityConfig, optional
        A VerbosityConfig controling what is logged during the execution
        of the program. Default is no verbosity.

    Attributes
    ----------
    instruction_set : InstructionSet
        The InstructionSet to use for executing programs.
    verbosity_config : VerbosityConfig, optional
        A VerbosityConfig controling what is logged during the execution
        of the program. Default is no verbosity.
    state : PushState
        The current PushState. Contains one stack for each PushType utilized
        mentioned by the instructions in the instruction set.
    status : PushInterpreterStatus
        A string denoting if the Interpreter has enountered a situation
        where non-standard termination was required.

    """

    def __init__(self,
                 instruction_set: Union[InstructionSet, str] = "core",
                 verbosity_config: VerbosityConfig = "default",
                 reset_on_run: bool = True):
        self.reset_on_run = reset_on_run
        # If no instruction set given, create one and register all instructions.
        if instruction_set == "core":
            self.instruction_set = InstructionSet(register_core=True)
        else:
            self.instruction_set = instruction_set

        self.type_library = self.instruction_set.type_library

        if verbosity_config == "default":
            self.verbosity_config = DEFAULT_VERBOSITY_LEVELS[0]
        else:
            self.verbosity_config = verbosity_config

        # Initialize the PushState and status
        self.state = None
        self.status = None
        self._verbose_trace = None
        self._log_fn_for_trace = None
        self._validate()
        self.reset()

    def _validate(self):
        library_type_names = set(self.type_library.keys())
        required_stacks = self.instruction_set.required_stacks() - {"stdout", "exec", "untyped"}
        if not required_stacks <= library_type_names:
            raise ValueError(
                "PushInterpreter instruction_set and type_library are incompatible. {iset} vs {tlib}. Diff: {d}".format(
                    iset=required_stacks,
                    tlib=library_type_names,
                    d=required_stacks - library_type_names,
                ))

    def reset(self):
        """Reset the interpreter status and PushState."""
        self.state = PushState(self.type_library)
        self.status = PushInterpreterStatus.normal
        self._verbose_trace = self.verbosity_config.program_trace
        self._log_fn_for_trace = log_function(self._verbose_trace)

    def _log_trace(self, msg=None, log_state=False):
        if msg is not None:
            self._log_fn_for_trace(msg)
        if log_state:
            self.state.pretty_print(self._log_fn_for_trace)

    def _evaluate_instruction(self, instruction: Union[Instruction, JitInstructionRef], config: PushConfig):
        self.state = instruction.evaluate(self.state, config)

    def untyped_to_typed(self):
        """Infers PushType of items on state's untyped queue and pushes to corresponding stacks."""
        while len(self.state.untyped) > 0:
            el = self.state.untyped.popleft()
            push_type = self.type_library.push_type_of(el, error_on_not_found=True)
            self.state[push_type.name].push(el)

    def evaluate_atom(self, atom: Atom, config: PushConfig):
        """Evaluate an Atom.

        Parameters
        ----------
        atom : Atom
            The Atom (Literal, Instruction, JitInstructionRef, or CodeBlock) to
            evaluate against the current PushState.
        config : PushConfig
            The configuration of the Push program being run.

        """
        try:
            if isinstance(atom, Instruction):
                self._evaluate_instruction(atom, config)
            elif isinstance(atom, JitInstructionRef):
                self._evaluate_instruction(self.instruction_set[atom.name], config)
            elif isinstance(atom, CodeBlock):
                for a in atom[::-1]:
                    self.state["exec"].push(a)
            elif isinstance(atom, Literal):
                if atom.push_type.is_collection or atom.push_type == PushStr:
                    if len(atom.value) > config.collection_size_cap:
                        return
                self.state[atom.push_type.name].push(atom.value)
            elif isinstance(atom, Closer):
                raise PushError("Closers should not be in push programs. Only genomes.")
            else:
                raise PushError("Cannot evaluate {t}, require a subclass of Atom".format(t=type(atom)))
            self.untyped_to_typed()
        except Exception as e:
            err_type = type(e).__name__
            err_msg = str(e)
            raise PushError(
                "{t} raised while evaluating {atom}. Original message: \"{m}\"".format(
                    t=err_type,
                    atom=atom,
                    m=err_msg
                ))

    def run(self,
            program: Program,
            inputs: list) -> list:
        """Run a Push program given some inputs and desired output PushTypes.

        The general flow of this method is:
            1. Create a new push state
            2. Load the program and inputs.
            3. If the exec stack is empty, return the outputs.
            4. Else, pop the exec stack and process the atom.
            5. Return to step 3.

        Parameters
        ----------
        program : Program
            Program to run.
        inputs : list
            A sequence of values to use as inputs to the push program.

        Returns
        -------
        Sequence
            A sequence of values pulled from the final push state. May contain
            pyshgp.utils.Token.no_stack_item if needed stacks are empty.

        """
        if self.reset_on_run:
            self.reset()

        push_config = program.signature.push_config

        # Setup
        self.state.load_code(program.code)
        self.state.load_inputs(inputs)
        stop_time = time.time() + push_config.runtime_limit
        steps = 0

        if self._verbose_trace >= self.verbosity_config.log_level:
            self._log_trace("Initial State:", True)

        # Iterate atom evaluation until entire program is evaluated.
        while len(self.state["exec"]) > 0:
            # Stopping conditions
            if steps > push_config.step_limit:
                self.status = PushInterpreterStatus.step_limit_exceeded
                break
            if time.time() > stop_time:
                self.status = PushInterpreterStatus.runtime_limit_exceeded
                break

            # Next atom in the program to evaluate.
            next_atom = self.state["exec"].pop()

            if self._verbose_trace >= self.verbosity_config.log_level:
                self._log_trace("Current Atom: " + str(next_atom))

            # Evaluate atom.
            old_size = self.state.size()
            self.evaluate_atom(next_atom, push_config)
            if self.state.size() > old_size + push_config.growth_cap:
                self.status = PushInterpreterStatus.growth_cap_exceeded
                break

            if self._verbose_trace >= self.verbosity_config.log_level:
                self._log_trace("Current State:", True)
            steps += 1

        if self._verbose_trace >= self.verbosity_config.log_level:
            self._log_trace("Finished program evaluation.")

        return self.state.observe_stacks(program.signature.output_stacks)


DEFAULT_INTERPRETER = PushInterpreter()
