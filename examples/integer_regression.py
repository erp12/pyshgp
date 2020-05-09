"""A simple regression problem using integer data."""

import logging
import random
import numpy as np
import sys

from pyshgp.gp.selection import Lexicase
from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet


def target_function(a, b):
    """Generate a training data point."""
    return (2 * a * b) + (b * b)


X = np.arange(50).reshape(-1, 2)
y = np.array([[target_function(x[0], x[1])] for x in X])

instruction_set = (
    InstructionSet()
    .register_core_by_stack({"int"}, exclude_stacks={"str", "exec", "code"})
)

spawner = GeneSpawner(
    n_inputs=2,
    instruction_set=instruction_set,
    literals=[],
    erc_generators=[
        lambda: random.randint(0, 10),
    ]
)


ep_lex_sel = Lexicase(epsilon=True)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stdout
    )

    est = PushEstimator(
        population_size=200,
        max_generations=50,
        simplification_steps=500,
        spawner=spawner,
        selector=ep_lex_sel,
        verbose=2
    )

    est.fit(X=X, y=y)
    print(est.solution.program)
    print(est.predict(X))
    print(est.score(X, y))
