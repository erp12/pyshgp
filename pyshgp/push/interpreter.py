"""The :mod:`interpreter` module defines the ``PushInterpreter`` used to run Push programs."""
from typing import Union
import time
from enum import Enum

from pyshgp.push.instruction import Instruction
from pyshgp.push.program import Program
from pyshgp.push.state import PushState
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.atoms import Atom, Closer, Literal, InstructionMeta, CodeBlock, Input
from pyshgp.push.config import PushConfig
from pyshgp.tap import tap
from pyshgp.validation import PushError


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
        The ``InstructionSet`` to use for executing programs. Default is "core"
        which instantiates an ``InstructionSet`` using all the core instructions.

    Attributes
    ----------
    instruction_set : InstructionSet
        The ``InstructionSet`` to use for executing programs.
    state : PushState
        The current ``PushState``. Contains one stack for each ``PushType``
        mentioned by the instructions in the instruction set.
    status : PushInterpreterStatus
        A string denoting if the interpreter has encountered a situation
        where non-standard termination was required.

    """

    def __init__(self,
                 instruction_set: Union[InstructionSet, str] = "core",
                 reset_on_run: bool = True):
        self.reset_on_run = reset_on_run
        # If no instruction set given, create one and register all instructions.
        if instruction_set == "core":
            self.instruction_set = InstructionSet(register_core=True)
        else:
            self.instruction_set = instruction_set

        self.type_library = self.instruction_set.type_library

        # Initialize the PushState and status
        self.state: PushState = None
        self.status: PushInterpreterStatus = None
        self._validate()

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

    def _evaluate_instruction(self, instruction: Instruction, config: PushConfig):
        self.state = instruction.evaluate(self.state, config)

    def untyped_to_typed(self):
        """Infer ``PushType`` of items on state's untyped queue and push to corresponding stacks."""
        while len(self.state.untyped) > 0:
            el = self.state.untyped.popleft()
            push_type = self.type_library.push_type_of(el, error_on_not_found=True)
            self.state[push_type.name].push(el)

    @tap
    def evaluate_atom(self, atom: Atom, config: PushConfig):
        """Evaluate an ``Atom``.

        Parameters
        ----------
        atom : Atom
            The Atom (``Literal``, ``InstructionMeta``, ``Input``, or ``CodeBlock``) to
            evaluate against the current ``PushState``.
        config : PushConfig
            The configuration of the Push program being run.

        """
        try:
            if isinstance(atom, InstructionMeta):
                self._evaluate_instruction(self.instruction_set[atom.name], config)
            elif isinstance(atom, Input):
                input_value = self.state.inputs[atom.input_index]
                self.state.untyped.append(input_value)
            elif isinstance(atom, CodeBlock):
                for a in atom[::-1]:
                    self.state["exec"].push(a)
            elif isinstance(atom, Literal):
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

    @tap
    def run(self,
            program: Program,
            inputs: list,
            print_trace: bool = False) -> list:
        """Run a Push ``Program`` given some inputs and desired output ``PushTypes``.

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
        print_trace : bool
            If True, each step of program execution will be summarized in stdout.

        Returns
        -------
        Sequence
            A sequence of values pulled from the final push state. May contain
            pyshgp.utils.Token.no_stack_item if output stacks are empty.

        """
        push_config = program.signature.push_config

        if self.reset_on_run or self.state is None:
            self.state = PushState(self.type_library, push_config)
            self.status = PushInterpreterStatus.normal

        # Setup
        self.state.load_code(program.code)
        self.state.load_inputs(inputs)
        stop_time = time.time() + push_config.runtime_limit
        steps = 0

        if print_trace:
            print("Initial State:")
            self.state.pretty_print()

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

            if print_trace:
                start = time.time()
                print("\nCurrent Atom: " + str(next_atom))

            # Evaluate atom.
            old_size = self.state.size()
            self.evaluate_atom(next_atom, push_config)
            if self.state.size() > old_size + push_config.growth_cap:
                self.status = PushInterpreterStatus.growth_cap_exceeded
                break

            if print_trace:
                duration = time.time() - start
                print("Current State (step {step}):".format(step=steps))
                self.state.pretty_print()
                print("Step duration:", duration)
            steps += 1

        if print_trace:
            print("Finished program evaluation.")

        return self.state.observe_stacks(program.signature.output_stacks)


DEFAULT_INTERPRETER = PushInterpreter()
