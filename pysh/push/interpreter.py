# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:26:32 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

import time
import copy # <- This one is actually needed.

from .. import utils as u
from .. import constants as c
from .. import exceptions as e

from . import state
from .instructions import io

class PyshInterpreter:
    '''Object that can run Push programs.

    Attributes:
        state: The push state.
        status: Status of the interpreter, this isn't used much yet.
    '''
    
    def __init__(self, inputs = None):
        self.state = state.PyshState()
        self.status = '_normal'

        if inputs != None:
            for i in inputs:
                self.state.stacks['_input'].push_item(i)
        
    def reset_pysh_state(self):
        self.state = state.PyshState()
        self.status = '_normal'
        
    def execute_instruction(self, instruction):
        '''Executes a push instruction or literal.

        Args:
            instruction: The instruction to the executed.
        '''
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
            io.handle_input_instruction(instruction, self.state)
        elif pysh_type == '_class_instruction':
            # If the instruction is an class_instruction, handle it.
            io.handle_vote_instruction(instruction, self.state)
        elif pysh_type == '_list':
            # If the instruction is a list, then decompose it.
            # Copy the list to avoid mutability madness
            instruction_cpy = copy.deepcopy(instruction)
            # Reverse the list.
            instruction_cpy.reverse()
            # Push all contents of the list to the ``exec`` stack.
            for i in instruction_cpy:
                self.state.stacks['_exec'].push_item(i)
        elif pysh_type == False:
            # If pysh type was not found, raise exception.
            raise e.UnknownPyshType(instruction) 
        else:
            # If here, instruction is a pysh literal and will be pushed
            # on to its corrisponding stack.
            self.state.stacks[pysh_type].push_item(instruction)
    
    def eval_push(self, print_steps):
        '''Executes the contents of the exec stack.
        
        Aborts prematurely if execution limits are exceeded. If execution limits are
        reached, status will be denoted.

        Args:
            print_steps (bool): Denotes if stack state should be printed.
        '''        
        iteration = 1
        time_limit = 0
        if c.global_evalpush_time_limit != 0:
            time_limit = time.time() + c.global_evalpush_time_limit
        
        while len(self.state.stacks['_exec']) > 0:        
            
            # Check for adnormal stops            
            if iteration > c.global_evalpush_limit:
                self.status = '_evalpush_limit_reached'
                break
            if time_limit != 0 and time.time() > time_limit:
                self.status = '_evalpush_time_limit_reached'
                break;
            
            # Advance program 1 step
            top_exec = self.state.stacks['_exec'].top_item()    # Get top exec item
            self.state.stacks['_exec'].pop_item()               # Remove top exec item
            self.execute_instruction(top_exec)
            
            # print steps
            if print_steps:
                print( "\nState after " + str(iteration) + " steps:")
                self.state.pretty_print()
            
            iteration += 1
    
    
    def run_push(self, code, print_steps=False):
        '''The top level method of the push interpreter.

        Calls eval-push between appropriate code/exec pushing/popping.

        Args:
            code: The push program to run.
            print_steps: Denotes if stack states should be printed.
        '''
        # If you don't copy the code, the reference to the program will be reversed and other bad things.
        code_copy = copy.deepcopy(code)
        self.state.stacks['_exec'].push_item(code_copy)
        self.eval_push(print_steps)
        if print_steps:
            print("=== Finished Push Execution ===")
