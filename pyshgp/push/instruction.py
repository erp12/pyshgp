# -*- coding: utf-8 -*-
"""
The :mod:`instruction` module provides classes for various kinds of Push
instructions that can be handled by the ``pyshgp`` Push interpreter.
"""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numbers


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

    def __init__(self, name, func, stack_types, parentheses=0):
        self.name = name
        self.func = func
        self.stack_types = stack_types
        # Specifies parens group. (0, 1, 2, etc)
        self.parentheses = parentheses

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
        if input_depth >= len(state.inputs) or input_depth < 0:
            msg = "Pysh state does not contain an input at index {}."
            raise ValueError(msg.format(input_depth))
        input_value = state.inputs[input_depth]
        state['_exec'].push(input_value)


class PyshSetOutputInstruction(PyshInstruction):
    """A push instruction that will set a particular output value to a new
    value.

    Parameters
    ----------
    output_index : str
         The name of the key on the output structure to assign a value to.

    output_type : str
         The name of the stack to copy values from.
    """

    def __init__(self, output_index, output_type):
        name = '_set_output_{i}{t}'.format(i=output_index, t=output_type)
        PyshInstruction.__init__(self, name, None, ['_output'])
        self.output_index = output_index
        self.output_type = output_type

    def __repr__(self):
        return str(self.name)

    def execute(self, state):
        """Executes the output instruction on the given PushState.

        Parameters
        ----------
        state : PushState
            The PushState to execute the input instruction on.
        """
        if len(state[self.output_type]) == 0:
            return
        output_value = state[self.output_type].ref(0)
        state.outputs[self.output_index] = output_value


class PyshReduceOutputInstruction(PyshInstruction):
    """A push instruction that will modify a particular output value based on
    the current value, a new value, and a reducer function.

    Parameters
    ----------
    output_index : str
         The name of the key on the output structure to assign a value to.

    output_type : str
         The name of the stack to copy values from.

    reducer : function
        A function that takes two arguments, the current output value and the
        top value from ``output_type`` stack. Function returns new output value.

<<<<<<< HEAD
    name : str
        A name for the reducer function.
    """

    def __init__(self, output_index, output_type, reducer, name):
        name = '_{name}_output_{i}{t}'.format(i=output_index, t=output_type,
                                              name=name)
        PyshInstruction.__init__(self, name, None, ['_output'])
        self.output_index = output_index
        self.output_type = output_type
        self.reducer = reducer

    def __repr__(self):
        return str(self.name)

    def execute(self, state):
        """Executes the output instruction on the given PushState.

        Parameters
        ----------
        state: PushState
            The PushState to execute the input instruction on.
        """
        if len(state[self.output_type]) == 0:
            return
        current = state.outputs[self.output_index]
        new = state[self.output_type].ref(0)
        if current is None:
            state.outputs[self.output_index] = new
        else:
            state.outputs[self.output_index] = self.reducer(current, new)


class PyshTweakOutputInstruction(PyshInstruction):
    """A push instruction that will tweak a particular output value using a
    function.

    Parameters
    ----------
    output_index: str
         The name of the key on the output structure to assign a value to.

    tweaker: function
        A function that takes one argument, the current output value, and
        returns the new output value.

    name: str
        A name for the tweaker function.
    """

    def __init__(self, output_index, tweaker, name):
        name = '_{name}_output_{i}'.format(name=name, i=output_index)
        PyshInstruction.__init__(self, name, None, ['_output'])
        self.output_index = output_index
        self.tweaker = tweaker

    def __repr__(self):
        return str(self.name)

    def execute(self, state):
        """Executes the output instruction on the given PushState.

        Parameters
        ----------
        state: PushState
            The PushState to execute the input instruction on.
        """
        if state.outputs[self.output_index] is None:
            return
        current = state.outputs[self.output_index]
        state.outputs[self.output_index] = self.tweaker(current)


def make_numeric_output_instructions(output, int_only=False):
    """Returns a list of instructions that treat the output value as numeric
    value that can be set or perturbed.

    Parameters
    ----------
    output: int
        Index of the output value to create output instructions for.

    int_only: bool, optional(default=False)
        If true, only returns instructions that utilize the integer stack.
    """
    instrs = [
        PyshSetOutputInstruction(output, '_integer'),
        PyshReduceOutputInstruction(
            output, '_integer', lambda x, y: x + y, '+')
    ]
    if not int_only:
        instrs = instrs + [
            PyshSetOutputInstruction(output, '_float'),
            PyshReduceOutputInstruction(output, '_float', lambda x, y: x + y,
                                        '+')
        ]
    return instrs


def make_classification_instructions(class_index):
    """Returns a list of instructions that treat the output value as a class to
    for for and against.

    Parameters
    ----------
    class_index: int
         An integer greater than or equal to 0.
    """
    return [
        PyshSetOutputInstruction(class_index, '_integer'),
        PyshSetOutputInstruction(class_index, '_float'),
        PyshReduceOutputInstruction(class_index, '_integer', lambda x, y: x + y,
                                    '+'),
        PyshReduceOutputInstruction(class_index, '_float', lambda x, y: x + y,
                                    '+'),
        PyshTweakOutputInstruction(class_index, lambda x: x + 1, 'inc'),
        PyshTweakOutputInstruction(class_index, lambda x: x - 1, 'dec')
    ]
