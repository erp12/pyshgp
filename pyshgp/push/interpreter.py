# -*- coding: utf-8 -*-

"""
The :mod:`interpreter` module defines the ``PushInterpreter`` class which is
capable of running Push programs.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import time
import copy # <- This one is actually needed.

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

    input_value = state['_input'].ref(input_depth)
    pysh_type = u.recognize_pysh_type(input_value)

    if pysh_type == '_instruction':
        state['_exec'].push_item(input_value)
    elif pysh_type == '_list':
        state['_exec'].push_item(input_value)
    else:
        state[pysh_type].push_item(input_value)

def _handle_vote_instruction(instruction, state):
    '''Allows Push to handle class voting instructions.
    '''
    if len(state[instruction.vote_stack]) > 0:
        class_index = int(instruction.class_id)
        vote_value = state[instruction.vote_stack].ref(0)
        state[instruction.vote_stack].pop_item()
        state['_output'][class_index] += float(vote_value)

class PushInterpreter:
    """Object that can run Push programs and stores the state of the Push
    stacks.
    """

    #: Current Push state of the interpreter.
    state = None

    #: Current status of the interpreter. Either '_normal' or some kind of
    #: error indicator.
    status = '_normal'


    def __init__(self, inputs = None):
        self.reset_state()
        self.status = '_normal'

        # Load inputs
        if not (inputs is None):
            for i in inputs:
                self.state['_input'].push_item(i)

    def reset_state(self):
        """Clears the Push state and resets status.
        """
        self.state = {}
        for t in c.pysh_types:
            self.state[t] = stack.PyshStack(t)
        self.status = '_normal'

    def state_size(self):
        """Returns the number of items on the stacks, not including output str.

        :returns: Int of size.
        """
        i = 0
        for stk in self.state.values():
            i += len(stk)
        # if output stack exists, subtract 1 from total because the
        # first element of the output stack is the printing string.
        if '_output' in self.state.keys():
            i -= 1
        return i

    def state_as_dict(self):
        """Returns the state as a python dictionary.

        :returns: Dict of all values in state.
        """
        dct = {}
        for k in self.state.keys():
            dct[k] = self.state[k][:]
        return dct

    def state_from_dict(self, state_dict):
        """Repalces the Push state with an Push state based on given dict.

        .. warning::
            This is written to be used in ``pyshgp`` tests, NOT as part of 
            push program execution or evolution. There are no checks to confirm
            that the ``state_dict`` can be converted to a valid Push state.

        :param dict state_dict: Dict that is converted into a Push state.
        """
        self.reset_state()
        for k in state_dict.keys():
            if k is '_output':
                stck = state_dict[k][1:]
            else:
                stck = state_dict[k][::]
            for val in stck:
                self.state[k].push_item(val)

    def state_pretty_print(self):
        '''Prints state of all stacks in the pysh_state
        '''
        for t in c.pysh_types:
            print(self.state[t].pysh_type, ":", self.state[t])

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
        elif pysh_type == '_class_vote_instruction':
            # If the instruction is an class_instruction, handle it.
            _handle_vote_instruction(instruction, self.state)
        elif pysh_type == '_list':
            # If the instruction is a list, then decompose it.
            # Copy the list to avoid mutability madness
            instruction_cpy = copy.deepcopy(instruction)
            # Reverse the list.
            instruction_cpy.reverse()
            # Push all contents of the list to the ``exec`` stack.
            for i in instruction_cpy:
                self.state['_exec'].push_item(i)
        elif pysh_type == False:
            # If pysh type was not found, raise exception.
            raise e.UnknownPyshType(instruction) 
        else:
            # If here, instruction is a pysh literal and will be pushed
            # on to its corrisponding stack.
            self.state[pysh_type].push_item(instruction)
    
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
            self.state['_exec'].pop_item()
            self.execute_instruction(top_exec)
            
            # print steps
            if print_steps:
                print( "\nState after " + str(iteration) + " steps:")
                self.state_pretty_print()
            
            iteration += 1
    
    
    def run_push(self, code, print_steps=False):
        """The top level method of the push interpreter.

        Calls eval-push between appropriate code/exec pushing/popping.

        :param list code: The push program to run.
        :param bool print_steps: Denotes if stack states should be printed.
        """
        # If you don't copy the code, the reference to the program will be 
        # reversed and other bad things.
        code_copy = copy.deepcopy(code)
        self.state['_exec'].push_item(code_copy)
        self.eval_push(print_steps)
        if print_steps:
            print("=== Finished Push Execution ===")

