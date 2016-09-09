# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:26:32 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type


import time

from . import pysh_state
from . import pysh_utils
from . import pysh_random
from . import pysh_globals as g
from .instructions import boolean, code, common, input_output, numbers, string
from .instructions import registered_instructions
from .instructions import input_output


class Pysh_Interpreter:
    '''
    Object that can run Push programs.
    '''
    
    def __init__(self):
        self.state = pysh_state.Pysh_State()
        self.status = '_normal'
        
    def reset_pysh_state(self):
        self.state = pysh_state.Pysh_State()
        self.status = '_normal'
        
    def execute_instruction(self, instruction):
        if instruction is None:
            return
        if callable(instruction):
            instruction = instruction()
        pysh_type = pysh_utils.recognize_pysh_type(instruction)
        if pysh_type == '_instruction':
            instruction.func(self.state)
        elif pysh_type == '_input_instruction':
            input_output.handle_input_instruction(instruction, self.state)
        elif pysh_type == '_list':
            instruction.reverse()
            for i in instruction:
                self.state.stacks['_exec'].push_item(i)
        elif pysh_type == False:
            raise Exception("Attempted to evaluate " + str(instruction) + " of type " + str(type(instruction)) + ". It isn't an instruction string or literal.") 
        else:
            self.state.stacks[pysh_type].push_item(instruction)
    
    def eval_push(self, print_steps):
        '''
        Executes the contents of the exec stack, aborting prematurely if execution limits are 
        exceeded. The resulting push state will map termination to _normal if termination was 
        normal, or _abnormal otherwise.
        '''        
        iteration = 1
        time_limit = 0
        if g.global_evalpush_time_limit != 0:
            time_limit = time.time() + g.global_evalpush_time_limit
        
        while len(self.state.stacks['_exec']) > 0:        
            
            # Check for adnormal stops            
            if iteration > g.global_evalpush_limit:
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
        '''
        The top level of the push interpreter; calls eval-push between appropriate code/exec 
        pushing/popping. The resulting push state will map :termination to :normal if termination was 
        normal, or :abnormal otherwise.
        '''
        self.state.stacks['_exec'].push_item(code)
        self.eval_push(print_steps)
        if print_steps:
            print("=== Finished Push Execution ===")
