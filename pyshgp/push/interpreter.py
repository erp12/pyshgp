# -*- coding: utf-8 -*-

"""
The :mod:`interpreter` module defines the ``PushInterpreter`` class which is
capable of running Push programs.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import time
from copy import deepcopy # <- This one is actually needed.
from collections import OrderedDict
import numpy as np

from .. import utils as u
from .. import constants as c
from .. import exceptions as e
from . import stack

def _handle_input_instruction(instruction, state):
    '''Allows Push to handle input instructions.
    '''
    input_depth = int(instruction.input_index)

    if input_depth >= len(state['_input']) or input_depth < 0:
        raise e.InvalidInputStackIndex(input_depth)

    input_value = state['_input'][input_depth]
    pysh_type = u.recognize_pysh_type(input_value)

    if pysh_type == '_instruction':
        state['_exec'].push(input_value)
    elif pysh_type == '_list':
        state['_exec'].push(input_value)
    else:
        state[pysh_type].push(input_value)

def _handle_output_instruction(instruction, state):
    """Allows Push to handle class output instructions.
    """
    if len(state[instruction.from_stack]) == 0:
        return
    output_value = state[instruction.from_stack].ref(0)
    state[instruction.from_stack].pop()
    state['_output'][instruction.output_name] = output_value

def _handle_vote_instruction(instruction, state):
    '''Allows Push to handle class voting instructions.
    '''
    output_name = 'class-'+instruction.class_id
    # if not output_name in state['_output'].keys():
    #     return
    vote_value = state[instruction.vote_stack].ref(0)
    state[instruction.vote_stack].pop()
    state['_output'][class_index] += float(vote_value)

class PushState(dict):
    """Dictionary that holds PyshStacks.
    """

    def __init__(self, inputs=[]):
        if not isinstance(inputs, (list, np.ndarray)):
            msg = "Push inputs must be a list, got {}"
            raise ValueError(msg.format(type(inputs)))
        self['_input'] = inputs[::-1]
        self['_output'] = OrderedDict()

        for t in c.pysh_types:
            self[t] = stack.PyshStack(t)

    def __len__(self):
        """Returns the size of the PushState.
        """
        return sum([len(s) for s in self.values()])

    def from_dict(self, d):
        """Sets the state to match the given dictionary.

        .. warning::
            This is written to be used in ``pyshgp`` tests, NOT as part of
            push program execution or evolution. There are no checks to confirm
            that the ``d`` can be converted to a valid Push state.

        :param dict d: Dict that is converted into a Push state.
        """
        # Clear existing stacks.
        self['_input'] = []
        for t in c.pysh_types:
            self[t] = stack.PyshStack(t)
        # Overwrite stacks found in dict
        for k in d.keys():
            if k == '_input' or k == '_output':
                # Make output field the same as dictionary. Should be a dict.
                self[k] = d[k]
            else:
                # Append all values from dictionary onto corrisponding stack.
                for v in d[k]:
                    self[k].push(v)

    def pretty_print(self):
        """Prints state of all stacks in the PushState.
        """
        for t in c.pysh_types:
            print(self[t].pysh_type, ":", self[t])
        print('_input :', self['_input'])
        print('_output :', self['_output'])

class PushInterpreter:
    """Object that can run Push programs and stores the state of the Push
    stacks.
    """

    #: Current PushState of the interpreter.
    state = None

    #: Current status of the interpreter. Either '_normal' or some kind of
    #: error indicator.
    status = '_normal'


    def __init__(self, inputs=[]):
        self.inputs = inputs
        self.state = PushState(inputs)
        self.status = '_normal'

    def reset(self):
        """Resets the PushInterpreter. Should be called between push program
        executions.
        """
        self.state = PushState(self.inputs)
        self.status = '_normal'

    def execute_instruction(self, instruction):
        """Executes a push instruction or literal.

        :param PushInstruction instruction: The instruction to the executed.
        """
        # If the instruction is None, return.
        if instruction is None:
            return

        # If the instruction is a callable function, call it to get a
        # value for ``instruction``.
        if callable(instruction):
            instruction = instruction()

        # Detect the pysh type of the instruction.
        pysh_type = u.recognize_pysh_type(instruction)

        if pysh_type == '_instruction':
            # If the instruction is a standard push instruction, call it's
            # function on the current push state.
            instruction.func(self.state)
        elif pysh_type == '_input_instruction':
            # If the instruction is an input_instruction, handle it.
            _handle_input_instruction(instruction, self.state)
        elif pysh_type == '_output_instruction':
            # If the instruction is an output instruction, handle it.
            _handle_output_instruction(instruction, self.state)
        elif pysh_type == '_class_vote_instruction':
            # If the instruction is an class_instruction, handle it.
            _handle_vote_instruction(instruction, self.state)
        elif pysh_type == '_list':
            # If the instruction is a list, then decompose it.
            # Copy the list to avoid mutability madness
            instruction_cpy = deepcopy(instruction)
            # Reverse the list.
            instruction_cpy.reverse()
            # Push all contents of the list to the ``exec`` stack.
            for i in instruction_cpy:
                self.state['_exec'].push(i)
        elif pysh_type == False:
            # If pysh type was not found, raise exception.
            raise e.UnknownPyshType(instruction)
        else:
            # If here, instruction is a pysh literal and will be pushed
            # on to its corrisponding stack.
            self.state[pysh_type].push(instruction)

    def eval_push(self, print_steps):
        """Executes the contents of the exec stack.

        Aborts prematurely if execution limits are exceeded. If execution
        limits are reached, status will be denoted.

        :param bool print_steps: Denotes if stack state should be printed.
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
                break;

            # Advance program 1 step
            top_exec = self.state['_exec'].top_item()
            self.state['_exec'].pop()
            self.execute_instruction(top_exec)

            # print steps
            if print_steps:
                print( "\nState after " + str(iteration) + " steps:")
                self.state.pretty_print()

            iteration += 1


    def run_push(self, code, print_steps=False):
        """The top level method of the push interpreter.

        Calls eval-push between appropriate code/exec pushing/popping.

        :param list code: The push program to run.
        :param bool print_steps: Denotes if stack states should be printed.
        """
        self.reset()
        # If you don't copy the code, the reference to the program will get
        # reversed and other bad things.
        code_copy = deepcopy(code)
        self.state['_exec'].push(code_copy)
        self.eval_push(print_steps)
        if print_steps:
            print("=== Finished Push Execution ===")
        if '_output' in self.state.keys():
            return self.state['_output']
        else:
            return {}
