# -*- coding: utf-8 -*-

"""
The :mod:`instruction` module provides classes for various kinds of Push
instructions that can be handled by the ``pyshgp`` Push interpreter.
"""

from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

from .instructions import registered_instructions as ri

class PyshInstruction(object):
    """A instruction for the push language.

    :param str name: A string name for the instruction.
    :param function func: The python function that manipulates a Push state in the desired way.
    :param list stack_types: List of related Pysh types.
    :param int parentheses: Specifies number of paren groups. (0, 1, 2, ... etc)
    """

    def __init__(self, name, func, stack_types = [], parentheses = 0):
        self.name = name
        self.func = func
        self.stack_types = stack_types
        self.parentheses = parentheses # Specifies parens group. (0, 1, 2, ... etc)
        
    def __eq__(self, other):
        if isinstance(other, PyshInstruction):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return self.name.__hash__()

    def __repr__(self):
        return str(self.name)

class PyshInputInstruction(PyshInstruction):
    """A push instruction that will handle input values.

    Input instructions which are generated based on initial state of the _input stack.

    :param int input_index: The index in the input stack to get value from.
    """

    def __init__(self, input_index):
        name = "_input" + str(input_index)
        PyshInstruction.__init__(self, name, None)
        self.input_index = input_index
        self.stack_types = '_input'
        
    def __repr__(self):
        return str(self.name)

class PyshClassVoteInstruction(PyshInstruction):
    """A push instruction that will handle Class Voting.

    Pulls from a numerical stack to add "votes" to an element of the output stack.
    Intended to be used in classification problems.

    :param int class_id:   The index in the output stack to place vote.
    :param str vote_stack: The numerical stack from which to pull a vote.
    """

    def __init__(self, class_id, vote_stack):
        PyshInstruction.__init__(self, "_vote"+str(class_id)+vote_stack, None)
        self.class_id = class_id
        self.vote_stack = vote_stack
        self.stack_types = '_class'
        
    def __repr__(self):
        return str(self.name)

class JustInTimeInstruction(PyshInstruction):
    """A callable object that, when processed in by the push interpreter,
    returns a specific registered instruction.

    Use of these instructions is only needed when defining new Push
    instructions that must call themselves, or other situations where a Push
    instruction must be defined in a way that creates an instance of another
    Push instruction that is not yet registered.

    """

    #: Name of the instruction to look up and use in place of this instruction
    #: during program execution.
    name = None

    def __init__(self, instruction_name):
        self.name = instruction_name

    def __call__(self):
        return ri.get_instruction(self.name)

    def __repr__(self):
        return self.name + "_JIT"
