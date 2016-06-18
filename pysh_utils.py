# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:36:03 2016

@author: Eddie
"""

import pysh_globals as g


def flatten_all(lst):
    result = []
    for i in lst:
        if type(i) == list:
            result += flatten_all(i)
        else:
            result += i
    return result


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
    if n > g.max_number_magnitude:
        n = g.max_number_magnitude
    elif n < -g.max_number_magnitude:
        n = -g.max_number_magnitude
    return n

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
            remaining = remaining[1:]
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


# def list_to_open_close_sequence(lst):
#     if type(lst) == list:
#         flatten_all
#     else:
#         return lst

# def open_close_sequence_to_list(sequence):
#     if not type(sequence) == list:
#         return sequence
#     elif len(sequence) == 0:
#         return []
#     else:
#         opens = len(filter(lambda x: x == '_open', sequence))
#         closes = len(filter(lambda x: x == '_close', sequence))
#         if not opens == closes:
#             raise Exception("open-close sequence must have equal numbers of :open and :close; this one does not:\n", sequence)

#         lst = []
#         for el in sequence:
            

#         if len(l) == 1:
#             return l[0]
#         else:
#             return l

def get_matcing_close_index(sequence):
    i = None
    open_count = 0
    for j in range(len(sequence)):
        if sequence[j] == '_open':
            open_count += 1
        elif sequence[j] == '_close':
            open_count -= 1
        if open_count == 0:
            return j
        j += 1

def open_close_sequence_to_list(sequence):
    if not type(sequence) == list:
        return sequence
    elif len(sequence) == 0:
        return []
    else:
        result = []
        rest = sequence
        while len(rest) > 0:
            if rest[0] == '_open':
                i = get_matcing_close_index(rest)
                sub_seq = rest[1:i]
                result.append( open_close_sequence_to_list(sub_seq) )
                rest = rest[i+1:]
            else:
                result.append(rest[0])
                rest.pop(0)
        return result



# print open_close_sequence_to_list(["_open", 1, 2, "_open", 'a', 'b', "_open", 'c', "_close", "_open", "_open", 'd', "_close", "_close", 'e', "_close", "_close"])
# print open_close_sequence_to_list(["_open", 1, "_close", "_open", 2, "_close"])
# print open_close_sequence_to_list(["_open", "_open", 1, "_close", "_open", 2, "_close", "_close"])









