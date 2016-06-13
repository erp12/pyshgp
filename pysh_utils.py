# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:36:03 2016

@author: Eddie
"""

import pysh_globals


def recognize_pysh_type(thing):
    '''
    If thing is a literal, return its type -- otherwise return False.
    '''
    if type(thing) is str and thing[0] == '_':
        return '_instruction'
    elif type(thing) is int:
        return '_integer'
    elif type(thing) is float:
        return '_float'
    elif type(thing) is str:
        return '_string'
    elif type(thing) is bool:
        return '_bool'
    elif type(thing) is list:
        return '_list'
    else:
        return False
    
        

def keep_number_reasonable(n):
    '''
    Returns a version of n that obeys limit parameters.
    '''
    if n > pysh_globals.max_number_magnitude:
        n = pysh_globals.max_number_magnitude
    elif n < -pysh_globals.max_number_magnitude:
        n = -pysh_globals.max_number_magnitude
    return 

def count_parens(tree):
    '''
    Returns the number of paren pairs in tree.
    '''
    remaining = tree
    total = 0

    while True:
        if type(remaining) != list:
            return total
        elif len(remaining) == 0:
            return total + 1
        elif type(remaining[0]) != list:
            remaining.pop(0)
        else:
            remaining = remaining[0] + remaining[1:]
            total

def count_points(tree):
    '''
    Returns the number of points in tree, where each atom and each pair of parentheses 
    counts as a point.
    '''
    remaining = tree
    total = 0

    while True:
        if type(remaining) != list:
            return total + 1
        elif len(remaining) == 0:
            return total + 1
        elif type(remaining[0]) != list:
            remaining.pop(0)
            total += 1
        else:
            remaining = remaining[0] + remaining[1:]
            total += 1
    return total
    

def reductions(f, l):
    '''
    Returns a list of the intermediate values of the reduction (as
    per reduce) of coll by f, starting with init.
    '''
    result = []
    for i in range(len(l)-1):
        if i > 0:
            result.append(l[i])
        else:
            result.append(f(l[i], l[i + 1]))
    return result





