# _*_ coding: utf_8 _*_
"""
Created on 5/21/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import cProfile, pstats, io
import numpy
import random

from pysh.gp import gp
from pysh import pysh_random as r

pr = cProfile.Profile()
pr.enable()

r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[1], gp.default_evolutionary_params)
r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[2], gp.default_evolutionary_params)
r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[3], gp.default_evolutionary_params)
r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[4], gp.default_evolutionary_params)
r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[5], gp.default_evolutionary_params)
r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[6], gp.default_evolutionary_params)
r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[7], gp.default_evolutionary_params)
r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[8], gp.default_evolutionary_params)
r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[9], gp.default_evolutionary_params)
r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[0], gp.default_evolutionary_params)


pr.disable()
s = io.StringIO()
sortby = 'cumulative'
ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
ps.print_stats()
print(s.getvalue())

#cProfile.run('[r.atom_to_plush_gene(list(gp.default_evolutionary_params["atom_generators"].keys())[7], gp.default_evolutionary_params) for x in range(5000)]', 'pysh_stats')
#p = pstats.Stats('pysh_stats')
#p.strip_dirs().sort_stats('time').print_stats()