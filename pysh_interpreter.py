# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:26:32 2016

@author: Eddie
"""

import time


import pysh_state
import registered_instructions
import pysh_globals
import pysh_utils

from instructions import *

class Pysh_Interpreter:
    '''
    
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
        pysh_type = pysh_utils.recognize_pysh_type(instruction)
        if pysh_type == '_instruction':
            instruction_obj = list(filter(lambda x: x.name == instruction[1:],
                                          registered_instructions.registered_instructions))[0]
            instruction_obj.func(self.state)
        elif pysh_type == '_list':
            instruction.reverse()
            for i in instruction:
                self.state.stacks['_exec'].push_item(i)
        elif pysh_type == False:
            raise Error("Attempted to evaluate something that isn't an instruction or literal.") 
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
        if pysh_globals.global_evalpush_time_limit != 0:
            time_limit = time.time() + pysh_globals.global_evalpush_time_limit
        
        while len(self.state.stacks['_exec']) > 0:        
            
            # Check for adnormal stops            
            if iteration > pysh_globals.global_evalpush_limit:
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
        self.reset_pysh_state()
        self.state.stacks['_exec'].push_item(code)
        self.eval_push(print_steps)
        
        self.state.pretty_print()
        
        
        
#pi = Pysh_Interpreter()
#print( registered_instructions.registered_instructions )

#test_program_1 = [1, 2, '_integer_add']

#pi.run_push(test_program_1)