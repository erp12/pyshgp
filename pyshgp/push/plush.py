# -*- coding: utf-8 -*-

"""
The :mod:`plush` module contains code pertaining the Plush genenomes.

Plush genomes are linear representations of Push programs.
Plush genomes are python lists of plush genes.
Plush genes are python objects defined below.
"""
from __future__ import absolute_import, division, print_function, unicode_literals
__metaclass__ = type

class Gene(object):

    #: An instance of the instruction class or a literal
    atom = None

    #: Denotes if the gene is holding a literal or an instruction.
    is_literal = None

    #: Denotes how many close parens to place after instruction in program.
    closes = None

    #: If true, do not include instruction in translated program.
    is_silent = None

    def __init__(self, atom, is_literal, closes, is_silent=False):
        self.atom = atom
        self.is_literal = is_literal
        self.closes = closes
        self.is_silent = is_silent

    def __repr__(self):
        return "Gene<{}, {}, {}, {}>".format(self.atom,
                                             self.is_literal,
                                             self.closes,
                                             self.is_silent)
