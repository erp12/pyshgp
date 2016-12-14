# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:36:03 2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import sys
import random

from . import exceptions as e
from .push import instruction as instr
from . import constants as c


##             ##
# Utility Types #
##             ##

class Character(object):
    '''Holds a string of length 1.

    Used to distinguish between string and char literals 
    in Push program interpretation.

    Attributes:
        char (str): string of length 1.
    '''
    def __init__(self, char):
        if len(char) == 0:
            raise e.EmptyCharacterException()
        if len(char) > 1:
            raise e.LongCharacterException()
        self.char = char

    def __repr__(self):
        if self.char == '\n':
          return 'c_newline'
        if self.char == ' ':
          return 'c_space'
        return "c_" + self.char

    def __eq__(self, other):
        if isinstance(other, Character):
          return self.char == other.char
        return False

class PushVector(list):
    '''List where elements are all of same pysh literal types.

    Attributes:
        typ (type): Python type that all elements must be.
    '''
    def __init__(self, lst, typ):
        self.typ = typ
        if typ == None:
            self.typ = '_exec'

        for el in lst:
            if type(el) == typ:
                self.append(el)
            else:
                raise e.PushVectorTypeException(typ, type(el))

class UnevaluatableStackResponse:
    '''Used as the superclass for other bad stack responses.
    '''
    def __repr__(self):
        return 'UNEVALUATABLE_STACK_RESPONSE'

class NoStackItem(UnevaluatableStackResponse):
    '''Used as a response when getting value from empty PushStack.
    '''
    def __repr__(self):
        return 'NO_STACK_ITEM'

class StackOutOfBounds(UnevaluatableStackResponse):
    '''Used as a response when getting value from empty PushStack.
    '''
    def __repr__(self):
        return 'NO_STACK_ITEM'


##                 ##
# Utility Functions #
##                 ##

def flatten_all(lst):
    '''Recursively flattens nested lists into a single list.

    Args:
        lst: nested lists

    Returns:
        Flattened lists.

    Examples: 
        >>> flatten_all([1, [2, 3, [4], 5]])
        [1, 2, 3, 4, 5]
    '''
    result = []
    for i in lst:
        if type(i) == list:
            result += flatten_all(i)
        else:
            result += i
    return result


def recognize_pysh_type(thing):
    '''If thing is a literal, return its type -- otherwise return False.

    Args:
        thing: anything!

    Returns:
        A string with a ``_`` as the first char. This is how Pysh types
        are denoted throughout the entire package.
        If there is no appropriate Pysh type, returns False.

    Examples:
        >>> recognize_pysh_type(True)
        '_bool'

        >>> recognize_pysh_type(77)
        '_integer'

        >>> recognize_pysh_type(abs)
        False
    '''
    if type(thing) == instr.PyshInputInstruction:
        return '_input_instruction'
    elif type(thing) == instr.PyshClassVoteInstruction:
        return '_class_instruction'
    elif type(thing) == instr.PyshInstruction:
        return '_instruction'
    elif type(thing) is int:
        return '_integer'
    elif type(thing) is float:
        return '_float'
    elif sys.version_info[0] == 3 and (type(thing) is str or type(thing) is bytes):
        return '_string'
    elif sys.version_info[0] == 2 and (type(thing) is str or type(thing) is unicode):
        return '_string'
    elif type(thing) == Character:
        return '_char'
    elif type(thing) is bool:
        return '_boolean'
    elif type(thing) is PushVector:
        t = recognize_pysh_type(thing.typ())
        return '_vector' + t
    elif type(thing) is list:
        return '_list'
    else:
        print("Could not find pysh type for", thing, "of type", type(thing))
        return False
    
        

def keep_number_reasonable(n):
    '''
    Returns a version of n that obeys limit parameters.
    '''
    if n > c.max_number_magnitude:
        n = c.max_number_magnitude
    elif n < -c.max_number_magnitude:
        n = -c.max_number_magnitude
    return n

def normalize_genetic_operator_probabilities(gen_op_dict):
    tot = sum(gen_op_dict.values())
    new_probs = [round(x / tot, 4) for x in gen_op_dict.values()]
    return dict(zip(gen_op_dict.keys(), new_probs))

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
    for i in range(len(l)):
        if i == 0:
            result.append(l[i])
        else:
            result.append(f(result[-1], l[i]))
    return result

# def list_to_open_close_sequence(lst):
#     if type(lst) == list:
#         flatten_all
#     else:
#         return lst


def get_matcing_close_index(sequence):
    open_count = 0
    for i in range(len(sequence)):
        if sequence[i] == '_open':
            open_count += 1
        elif sequence[i] == '_close':
            open_count -= 1
        if open_count == 0:
            return i
        i += 1

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
# print(open_close_sequence_to_list(["_open", 1, 2, "_open", 'a', 'b', "_open", 'c', "_close", "_open", "_open", 'd', "_close", "_close", 'e', "_close", "_close"]))
# print(open_close_sequence_to_list(["_open", 1, "_close", "_open", 2, "_close"]))
# print(open_close_sequence_to_list(["_open", "_open", 1, "_close", "_open", 2, "_close", "_close"]))


def merge_dicts(*dict_args):
    '''
    Given any number of dicts, shallow copy and merge into a new dict,
    precedence goes to key value pairs in latter dicts.
    Taken From: http://stackoverflow.com/a/26853961/4297413 Thanks to Aaron Hall
    '''
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result

def merge_sets(*set_args):
    '''Given any number of sets, shallow copy and merge into a new set.
    '''
    result = set()
    for s in set_args:
        result.update(s)
    return result

def ensure_list(thing):
    if type(thing) == list:
        return thing
    else:
        return [thing]

def levenshtein_distance(s1, s2):
    '''
    Big thanks to: https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance#Python
    '''
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]

def test_and_train_data_from_domains(domains):
    '''
    Takes a list of domains and creates a set of (random) train inputs and a set of test
    inputs based on the domains. Returns [train test]. A program should not
    be considered a solution unless it is perfect on both the train and test cases.
    '''
    train_set = []
    test_set = []

    for d in domains:
        num_train = d["train_test_split"][0]
        num_test = d["train_test_split"][1]

        inpts = d["inputs"]
        if callable(inpts):
            inpts = [inpts() for x in range(num_train+num_test)]
        else:
            inpts = inpts[:]

        random.shuffle(list(inpts))
        train_set += inpts[:num_train]
        test_set += inpts[-num_test:]

    return [train_set, test_set]

def int_to_char(i):
    '''Convert ints to chars and only get human readable chars
    '''
    i = (i + 32) % 128
    return chr(i)

