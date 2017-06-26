# -*- coding: utf-8 -*-

"""
The :mod:`instruction` module provides classes for various kinds of Push
instructions that can be handled by the ``pyshgp`` Push interpreter.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import numbers

from .instructions import registered_instructions as ri
from ..exceptions import InvalidInputStackIndex


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

    def execute(self, state):
        """Executes the input instruction on the given PushState.

        Parameters
        ----------
        state : PushState
            The PushState to execute the input instruction on.
        """
        self.func(state)


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

    def execute(self, state):
        """Executes the input instruction on the given PushState.

        Parameters
        ----------
        state : PushState
            The PushState to execute the input instruction on.
        """
        input_depth = int(self.input_index)

        if input_depth >= len(state['_input']) or input_depth < 0:
            raise InvalidInputStackIndex(input_depth)

        input_value = state['_input'][input_depth]
        state['_exec'].push(input_value)


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

    def execute(self, state):
        """Executes the output instruction on the given PushState.

        Parameters
        ----------
        state : PushState
            The PushState to execute the input instruction on.
        """
        if len(state[self.from_stack]) == 0:
            return
        output_value = state[self.from_stack].ref(0)
        state['_output'][self.output_name] = output_value


class PyshClassVoteInstruction(PyshInstruction):
    """A push instruction that will handle Class Voting. Pulls from a numerical
    stack to add "votes" to an element of the output stack. Intended to be used
    in classification problems.

    Parameters
    ----------
    class_id : int
         The class number to vote for.

    vote : int, float, or str
        If ``int`` or ``float``, the amount to vote. If ``str`` the name of the
        numeric stack to take vote from.
    """

    def __init__(self, output_name, vote):
        PyshInstruction.__init__(self, "_vote_{}_{}".format(output_name, vote),
                                 None, ['_output'])
        self.output_name = output_name
        self.vote = vote
        self.stack_types = '_vote'

    def __repr__(self):
        return str(self.name)

    def execute(self, state):
        """Executes the class vote instruction on the given PushState.

        Parameters
        ----------
        state : PushState
            The PushState to execute the input instruction on.
        """
        if not self.output_name in state['_output'].keys():
            state['_output'][self.output_name] = 0.0
        vote_value = self.vote
        if isinstance(vote_value, numbers.Number):
            state['_output'][self.output_name] += float(vote_value)
        else:
            if len(state[vote_value]) > 0:
                v = state[vote_value].ref(0)
                state[vote_value].pop()
                state['_output'][self.output_name] += float(v)


def make_vote_instruction_set(classes):
    """Returns a list of PyshClassVoteInstruction instances that vote for and
    against a each class.

    Parameters
    ----------
    classes : list of str
         A list of class names.
    """
    vote_instrs = []
    for c in classes:
        vote_instrs += [
            PyshClassVoteInstruction(c, 1),
            PyshClassVoteInstruction(c, 2),
            PyshClassVoteInstruction(c, 4),
            PyshClassVoteInstruction(c, -1),
            PyshClassVoteInstruction(c, -2),
            PyshClassVoteInstruction(c, -4),
            PyshClassVoteInstruction(c, '_integer'),
            PyshClassVoteInstruction(c, '_float'),
        ]
    return vote_instrs


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
