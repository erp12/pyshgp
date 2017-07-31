# _*_ coding: utf_8 _*_
"""
Tests start to finish usage of PushGPRegressor class.
"""
import numpy as np

from pyshgp.gp.evolvers import PushGPRegressor


def target_function(x):
    return x**3 - (2 * (x**2)) - x


X_t = np.arange(0, 1, 0.1).reshape(-1, 1)
y_t = np.array([target_function(x) for x in X_t]).reshape(-1, 1)

model = PushGPRegressor(population_size=100, max_generations=5,
                        simplification_steps=500)
model.fit(X_t, y_t)
model.predict(X_t)
