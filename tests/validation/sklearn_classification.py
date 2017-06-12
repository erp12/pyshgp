# _*_ coding: utf_8 _*_
"""
@author: Eddie

Tests PushGPClassifier class
"""
from __future__ import absolute_import, division, print_function, unicode_literals

from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import numpy as np

import pyshgp.gp.base as gp


iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target,
                                                    test_size=0.5)

model = gp.PushGPClassifier(population_size = 100, max_generations = 5,
	simplification_steps = 500)
model.fit(X_train, y_train)
