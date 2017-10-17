# -*- coding: utf-8 -*-
"""
The :mod:`instruction` module provides classes for various kinds of Push
instructions that can be handled by the ``pyshgp`` Push interpreter.
"""


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
