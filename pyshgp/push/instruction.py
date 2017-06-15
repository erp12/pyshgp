# -*- coding: utf-8 -*-

"""
The :mod:`instruction` module provides classes for various kinds of Push
instructions that can be handled by the ``pyshgp`` Push interpreter.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from .instructions import registered_instructions as ri

class PyshInstruction(object):
    """A instruction for the push language.

    Parameters
    ----------
    nane : str
         A string name for the instruction.
    func : function
        The python function that manipulates a Push state in the desired way.
    stack_types : list of str
        List of related pyshgp types.
    parentheses : int
        Specifies number of paren groups. (0, 1, 2, ... etc)
    """

    def __init__(self, name, func, stack_types, parentheses = 0):
        self.name = name
        self.func = func
        self.stack_types = stack_types
        self.parentheses = parentheses # Specifies parens group. (0, 1, 2, etc)

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
    """A push instruction that will handle input values. Input instructions
    which are generated based on initial state of the _input stack.

    Parameters
    ----------
    input_index : int
         The index in the input stack to get value from.
    """

    def __init__(self, input_index):
        name = "_input" + str(input_index)
        PyshInstruction.__init__(self, name, None, ['_input'])
        self.input_index = input_index
        self.stack_types = '_input'

    def __repr__(self):
        return str(self.name)

class PyshOutputInstruction(PyshInstruction):
    """A push instruction that will handle output values.

    Parameters
    ----------
    output_name : str
         The name of the key on the output structure to assign a value to.

    from_stack : str
         The name of the stack to copy values from.
    """

    def __init__(self, output_name, from_stack):
        name = '_output'+from_stack+'_as_'+output_name
        PyshInstruction.__init__(self, name, None, ['_output'])
        self.output_name = output_name
        self.from_stack = from_stack

    def __repr__(self):
        return str(self.name)

class PyshClassVoteInstruction(PyshInstruction):
    """A push instruction that will handle Class Voting. Pulls from a numerical
    stack to add "votes" to an element of the output stack. Intended to be used
    in classification problems.

    Parameters
    ----------
    class_id : int
         The class number to vote for.

    vote_stack : str
        The numerical stack from which to pull a vote.
    """

    def __init__(self, class_id, vote_stack):
        PyshInstruction.__init__(self, "_vote"+str(class_id)+vote_stack,
                                 None, ['_output'])
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

    Parameters
    ----------
    instruction_name : str
         The name of the instruction to look-up and run when this JiT
         instruction is called.
    """

    def __init__(self, instruction_name):
        self.name = instruction_name

    def __call__(self):
        """
        When the JiT instruction is called, it returns the registered
        instruction by the same name.
        """
        return ri.get_instruction(self.name)

    def __repr__(self):
        return self.name + "_JIT"
