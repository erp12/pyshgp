"""The goal of the Odd problem is to evolve a program that will produce a True if
the input integer is odd, and a False if its even.
"""
import numpy as np
from pyshgp.gp.estimators import PushEstimator

X = np.arange(-10, 10).reshape(-1, 1)
y = [bool(x % 2) for x in X]

est = PushEstimator(population_size=1000, max_generations=200)
est.fit(X, y, True)

if __name__ == "__main__":
    print(est._result.program)
    print(est.predict(X))
    print(est.score(X, y))
