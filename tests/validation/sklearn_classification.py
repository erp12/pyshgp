# _*_ coding: utf_8 _*_
"""
Tests start to finish usage of PushGPClassifier class.
"""
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from pyshgp.gp.evolvers import PushGPClassifier


iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target,
                                                    test_size=0.5)

model = PushGPClassifier(population_size=20, max_generations=5,
                         simplification_steps=500)
model.fit(X_train, y_train)
model.predict(X_test)
