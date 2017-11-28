# -*- coding: utf-8 -*-

"""
The :mod:`plush` module contains code pertaining the Plush genenomes.

Plush genomes are linear representations of Push programs.
Plush genomes are python lists of plush genes.
Plush genes are python objects defined below.
"""


class Gene(object):
    """
    Attributes
    ----------
    atom : {Instruction, literal}
        An instance of the instruction class or a literal
    is_literal : bool
        Denotes if the gene is holding a literal or an instruction.
    closes : int
        Denotes how many close parens to place after instruction in program.
    is_silent : bool, optional
        If true, do not include instruction in translated program.
    """

    def __init__(self, atom, is_literal, closes=0, is_silent=False):
        self.atom = atom
        self.is_literal = is_literal
        self.closes = closes
        self.is_silent = is_silent

    def __repr__(self):
        return "Gene<{}, {}, {}, {}>".format(self.atom,
                                             self.is_literal,
                                             self.closes,
                                             self.is_silent)
