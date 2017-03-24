# _*_ coding: utf_8 _*_
"""
The :mod:`base` module defines the basic classes used to perform GP with
``pyshgp``.
"""

import params as p

from .. import utils as u


class Evolver:
    """Evolves push programs.
    """

    params = p.default_evolutionary_params