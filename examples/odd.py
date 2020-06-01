"""The Odd problem.

The goal of the Odd problem is to evolve a program that will produce a True if
the input integer is odd, and a False if its even.
"""
import numpy as np
import random
from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner


X = np.arange(-10, 10).reshape(-1, 1)
y = [[bool(x % 2)] for x in X]


spawner = GeneSpawner(
    n_inputs=1,
    instruction_set="core",
    literals=[],
    erc_generators=[lambda: random.randint(0, 10)]
)


if __name__ == "__main__":
    est = PushEstimator(
        spawner=spawner,
        population_size=300,
        max_generations=100,
        verbose=2
    )

    est.fit(X, y)
    print(est.solution.program)
    print(est.predict(X))
    print(est.score(X, y))
