# _*_ coding: utf_8 _*_
"""
Created on 5/21/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cProfile
import pstats
import numpy

from pysh.gp import gp
from pysh import pysh_random as r

#cProfile.run('[r.random_plush_genome_with_size(500, gp.default_evolutionary_params) for x in range(10)]', 'pysh_stats')

#cProfile.run('[r.atom_to_plush_gene(gp.default_evolutionary_params["atom_generators"][3], gp.default_evolutionary_params) for x in range(5000)]', 'pysh_stats')

cProfile.run('gp.generate_random_population(gp.default_evolutionary_params)')

p = pstats.Stats('pysh_stats')
p.strip_dirs().sort_stats('time').print_stats()