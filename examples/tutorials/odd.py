"""The goal of the Odd problem is to evolve a program that will produce a True if
the input integer is odd, and a False if its even.
"""
import logging
import numpy as np
import random
import sys
from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet


X = np.arange(-10, 10).reshape(-1, 1)
y = [[bool(x % 2)] for x in X]


instruction_set = (
    InstructionSet(register_all=True)
    .register_n_inputs(X.shape[1])
)

spawner = GeneSpawner(
    instruction_set=instruction_set,
    literals=[],
    erc_generators=[lambda: random.randint(0, 10)]
)

est = PushEstimator(
    spawner=spawner,
    population_size=500,
    max_generations=200,
    verbose=2
)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stdout
    )
    est.fit(X, y)
    print(est._result.program)
    print(est.predict(X))
    print(est.score(X, y))
