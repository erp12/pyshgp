# -*- coding: utf-8 -*-
"""
Created on Sun Jun  5 15:34:38 2016

@author: Eddie
"""

# Forces this directory to become a python package.

# Loads in all instruction files.
from os.path import dirname, basename, isfile
import glob
modules = glob.glob(dirname(__file__)+"/*.py")
l = [ basename(f)[:-3] for f in modules if isfile(f)]
l.remove('__init__')
l.remove('registered_instructions')
__all__ = l