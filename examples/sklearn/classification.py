# _*_ coding: utf_8 _*_
"""
@author: Eddie

This example problem is meant to be a demonstration of how ``pyshgp`` could be
used to perform simple classification tasks.

The problem consists of predicting the species of iris.
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

from pyshgp.gp.evolvers import PushGPClassifier


iris = datasets.load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target,
                                                    test_size=0.5)
clf = PushGPClassifier(population_size=100,
                       max_generations=10,
                       n_jobs=-1, verbose=2)
clf.fit(X_train, y_train)
y_hat = clf.predict(X_test)
print("accuracy:", accuracy_score(y_test, y_hat))

#
# Plotting
#

h = .02
x_min, x_max = X_test[:, 0].min() - 1, X_test[:, 0].max() + 1
y_min, y_max = X_test[:, 1].min() - 1, X_test[:, 1].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                     np.arange(y_min, y_max, h))
Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

fig = plt.figure(1, figsize=(8, 6))
plt.contourf(xx, yy, Z, cmap=plt.cm.coolwarm, alpha=0.8)
plt.scatter(X_test[:, 0], X_test[:, 3], c=y_test, cmap=plt.cm.coolwarm)
plt.xlabel('Feat1')
plt.ylabel('Feat2')
plt.show()
