# _*_ coding: utf_8 _*_
"""
@author: Eddie

This example problem is meant to be a demonstration of how ``pyshgp`` could be
used to perform simple classification tasks. 

The problem consists of predicting the species of iris.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from sklearn import datasets
import numpy as np

import pyshgp.gp.base as gp


iris = datasets.load_iris()
X_t = iris.data
y_t = iris.target

print(X_t)
print(y_t)
print()

model = gp.PushGPClassifier(population_size = 250)
model.fit(X_t, y_t)