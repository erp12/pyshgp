# -*- coding: utf-8 -*-

"""
The :mod:`interpreter` module defines the ``PushInterpreter`` class which is
capable of running Push programs.
"""
import time
# from copy import deepcopy  # <- This one is actually needed.
# from collections import OrderedDict
import numpy as np

from ..utils import recognize_pysh_type
from .. import constants as c
from .. import exceptions as e
from . import stack


class PushState(dict):
    """Custom dictionary that holds stacks of Pysh types. Includes methods to
    help with for push program execution.
    """

    def __init__(self):
        self.stdout = ''

        for t in c.pysh_types:
            self[t] = stack.PyshStack(t)

    def __len__(self):
        """Returns the size of the PushState.
        """
        return (sum([len(s) for s in self.values()]) + len(self.inputs))

    def load_inputs(self, inputs):
        """Loads a list of input values onto the PushState intputs.

        Parameters
        ----------
        inputs : list
            List of input values.
        """
        if not isinstance(inputs, (list, np.ndarray)):
            raise ValueError(
                "Push inputs must be a list, got {t}".format(t=type(inputs)))
        self.inputs = inputs[::-1]

    def observe_outputs(self, output_types):
        """Returns a list of output values based on the types indicated in
        ``output_types``. Items are take from the tops of each stack. If
        multiple occurences of the same type are in ``output_types``, the
        returned values are taken from progressively deeper in that stack. Does
        not pop the values off the stacks.

        Parameters
        ----------
        output_types : list
            List of strings denoting the pysh types of the returned values.
        """
        outputs = []
        counts = {}
        for typ in output_types:
            if typ in counts.keys():
                ndx = counts[typ]
                outputs.append(self.state[typ].ref(ndx))
                counts[typ] += 1
            else:
                outputs.append(self.state[typ].ref(0))
                counts[typ] = 1
        return outputs

    def from_dict(self, d):
        """Sets the state to match the given dictionary.

        .. warning::
            This is written to be used in ``pyshgp`` tests, NOT as part of
            push program execution or evolution. There are no checks to confirm
            that the ``d`` can be converted to a valid Push state.

        Parameters
        ----------
        d : dict
            Dict that is converted into a Push state.
        """
        # Clear existing stacks.
        for t in c.pysh_types:
            self[t] = stack.PyshStack(t)
        # Overwrite stacks found in dict
        for k in d.keys():
            if k == '_input':
                self.inputs = d[k]
            elif k == '_stdout':
                self.stdout += d[k]
            else:
                # Append all values from dictionary onto corrisponding stack.
                for v in d[k]:
                    self[k].push(v)

    def pretty_print(self):
        """Prints state of all stacks in the PushState.
        """
        for t in c.pysh_types:
            print(self[t].pysh_type, ":", self[t])
        print('Inputs :', self.inputs)
        print('Stdout :', self.stdout)


class PushInterpreter:
    """Object that can run Push programs and stores the state of the Push
    stacks.

    Parameters
    ----------
    inputs : list
        A list of all values that should be accessible as inputs.

    Attributes
    ----------
    state : PushState
        A :mod:`PushState` that hold the current state of all of the stacks.

    status : str
        Current status of the interpreter. Either '_normal' or some kind of
        error indicator.
    """

    def __init__(self):
        self.reset()

    def reset(self):
        """Resets the PushInterpreter. Should be called between push program
        executions.
        """
        self.state = PushState()
        self.status = '_normal'

    def eval_atom(self, instruction):
        """Executes a push instruction or literal.

        Parameters
        ----------
        instruction : PushInstruction
            The instruction to the executed.
        """
        # If the instruction is None, return.
        if instruction is None:
            return

        # If the instruction is a callable function, call it to get a
        # value for ``instruction``.
        if callable(instruction):
            instruction = instruction()

        # Detect the pysh type of the instruction.
        pysh_type = recognize_pysh_type(instruction)

        if pysh_type == '_instruction':
            # If the instruction is a standard push instruction, call it's
            # function on the current push state.
            instruction.execute(self.state)
        elif pysh_type == '_list':
            # If the instruction is a list, then decompose it. Copy the list to
            # avoid mutability madness and then reverse the list and  push all
            # contents of the list to the ``exec`` stack.
            for i in instruction[::-1]:
                self.state['_exec'].push(i)
        elif not pysh_type:
            # If pysh type was not found, raise exception.
            raise e.UnknownPyshType(instruction)
        else:
            # If here, instruction is a pysh literal and will be pushed
            # on to its corrisponding stack.
            self.state[pysh_type].push(instruction)

    def eval_push(self, print_steps=False):
        """Executes the contents of the exec stack.

        Aborts prematurely if execution limits are exceeded. If execution
        limits are reached, status will be denoted.

        Parameters
        ----------
        print_steps : bool, optional
            Denotes if stack state should be printed.
        """
        iteration = 1
        time_limit = 0
        if c.global_evalpush_time_limit != 0:
            time_limit = time.time() + c.global_evalpush_time_limit

        while len(self.state['_exec']) > 0:

            # Check for adnormal stops
            if iteration > c.global_evalpush_limit:
                self.status = '_evalpush_limit_reached'
                break
            if time_limit != 0 and time.time() > time_limit:
                self.status = '_evalpush_time_limit_reached'
                break

            # Advance program 1 step
            top_exec = self.state['_exec'].top_item()
            self.state['_exec'].pop()
            self.eval_atom(top_exec)

            # print steps
            if print_steps:
                print("\nState after " + str(iteration) + " steps:")
                self.state.pretty_print()

            iteration += 1

    def run(self, code, inputs, print_steps=False):
        """The top level method of the push interpreter.

        Calls eval-push between appropriate code/exec pushing/popping.

        Parameters
        ----------
        code : list
            The push program to run.
        print_steps : bool, optional
            Denotes if stack states should be printed.

        Returns
        -------
        Returns the output structure as a dictionary.
        """
        self.reset()
        # If you don't copy the code, the reference to the program will get
        # reversed and other bad things.
        code_copy = code[:]
        self.state['_exec'].push(code_copy)
        self.state.load_inputs(inputs)
        self.eval_push(print_steps)

        if print_steps:
            print("=== Finished Push Execution ===")

        return self.state.observe_outputs()
