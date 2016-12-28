# -*- coding: utf-8 -*-
"""
Created on Dec. 11, 2016

@author: Eddie
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
	'''
	'''
	def __init__(self, name):
		super(UnknownInstructionName, self).__init__('No registered instruction with name: ' + str(name))

##                       ##
# Utility Type Exceptions #
##                       ##

class UnknownGeneticOperator(Exception):
	'''
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