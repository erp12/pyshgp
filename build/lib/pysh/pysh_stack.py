# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 13:18:57 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals


class Pysh_Stack(list):
    
    def __init__(self, string_of_type):
        self.pysh_type = string_of_type
        if string_of_type == "_output":
            self.push_item("")
        
    def push_item(self, value):
        self.append(value)
        
    def pop_item(self):
        self.pop();
    
    def top_item(self):
        if len(self) > 0:        
            return self[-1]
        else:
            return '_no_stack_item'
    
    def stack_ref(self, position):
        if len(self) <= position:
            return '_stack_out_of_bounds_item'
        elif len(self) == 0:
            return '_no_stack_item'
        else:
            return self[(len(self) - 1) - position]
        
    def stack_insert(self, position, value):
        self.insert(position, value)

    def stack_flush(self):
        self = Pysh_Stack(self.pysh_type)