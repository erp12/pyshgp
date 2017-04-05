# _*_ coding: utf_8 _*_
"""
@author: Eddie

This example problem is meant to be a demonstration of how ``pyshgp`` could be
used to perform simple classification tasks. 

The problem consists of predicting the species of iris.
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from sklearn import datasets, model_selection
import numpy as np

import pyshgp.gp.base as gp


iris = datasets.load_iris()
X_train, X_test, y_train, y_test = model_selection.train_test_split(iris.data,
                                                                    iris.target,
                                                                    test_size=0.5)

print(X_train)
print(y_train)
print()

model = gp.PushGPClassifier(population_size = 100)
model.fit(X_train, y_train)