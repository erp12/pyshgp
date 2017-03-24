# -*- coding: utf-8 -*-
"""The :mod:`exceptions` module provides utility classes that inherit from
python Exception class. These errors can be used to provide more useful 
debugging information to the user.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

##                           ##
# Push Interpreter Exceptions #
##                           ##

class UnknownPyshType(Exception):
	'''Exception when a pysh type is expected.
	'''
	def __init__(self, thing):
		super(UnknownPyshType, self).__init__('Unkown pysh type for ' + str(thing) + '.')

class UnkownEpigeneticMarker(Exception):
	'''Exception when a unknown epigenetic marker is found.
	'''
	def __init__(self, marker):
		super(UnkownEpigeneticMarker, self).__init__('Unknown epigenetic marker: ' + str(marker))

class UnknownInstructionName(Exception):
	'''Exception when there is no registered instruction with given name.
	'''
	def __init__(self, name):
		super(UnknownInstructionName, self).__init__('No registered instruction with name: ' + str(name))

class UnknownPyshStack(Exception):
	'''Exception when a pysh state is asked to return an unknown 
	'''
	def __init__(self, stack_name):
		super(UnknownPyshStack, self).__init__('Pysh state does not contain stack ' + str(stack_name) + '.')

class InvalidInputStackIndex(Exception):
	'''Exception when an invalid index to the input stack is used to get element on input stack.
	'''
	def __init__(self, ind):
		super(InvalidInputStackIndex, self).__init__('Pysh state does not contain an input at index ' + str(ind) + '.')

##                       ##
# Utility Type Exceptions #
##                       ##

class UnknownGeneticOperator(Exception):
	'''Exception that is raised when an unknown genetic operator is specified.
	'''
	def __init__(self, name):
		super(UnknownGeneticOperator, self).__init__('Unknown genetic operator (or selection method) ' + str(name))

##                       ##
# Utility Type Exceptions #
##                       ##

class EmptyCharacterException(Exception):
	'''Exception that is raised when a Character object is empty.
	'''
	def __init__(self):
		super(EmptyCharacterException, self).__init__('Character object cannot be created from empty string.')

class LongCharacterException(Exception):
	'''Exception that is raised when a Character object is too long.
	'''
	def __init__(self):
		super(LongCharacterException, self).__init__('Character object cannot be created from string of length > 1.')

class PushVectorTypeException(Exception):
	'''Excepton that is raised when a element of an incorrect type is added to a PushVector.
	'''
	def __init__(self, vec_typ, el_typ):
		super(PushVectorTypeException, self).__init__(str(el_typ) + ' cannot be added to PushVector of type ' + str(vec_typ) + '.')