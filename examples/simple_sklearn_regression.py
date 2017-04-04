# _*_ coding: utf_8 _*_
"""
@author: Eddie

This example problem is meant to be a demonstration of how ``pyshgp`` could be
used to perform simple regression tasks. 

The problem consists of fitting the following polynomial: 

.. literalinclude:: /../examples/simple_sklearn_regression.py
   :pyobject: target_function

The training set for this problem consists of only 10 data points.

"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random
import numpy as np

import pyshgp.gp.base as gp


def target_function(x):
    return x**3 - (2*(x**2)) - x

X_t = np.arange(0, 1, 0.1)
y_t = np.array([target_function(x) for x in X_t])

print(X_t)
print(y_t)
print()

model = gp.PushGPRegressor(population_size = 250)
model.fit(X_t, y_t)