# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:39:36 2016

@author: Eddie
"""

class Pysh_Instruction(object):
    
    def __init__(self, name, func, stack_types = [], parentheses = 0):
        self.name = name
        #self.pysh_type = pysh_type
        self.func = func
        self.stack_types = stack_types
        self.parentheses = parentheses # Specifies parens group. (0, 1, 2, ... etc)
        
    def __repr__(self):
        return self.name
    
    