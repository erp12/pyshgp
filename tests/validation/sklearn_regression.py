# _*_ coding: utf_8 _*_
"""
@author: Eddie

Tests PushGPRegressor class
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import numpy as np

import pyshgp.gp.base as gp


def target_function(x):
    return x**3 - (2*(x**2)) - x

X_t = np.arange(0, 1, 0.1)
y_t = np.array([target_function(x) for x in X_t])

model = gp.PushGPRegressor(population_size = 100, max_generations = 5,
	final_simplification_steps = 500)
model.fit(X_t, y_t)