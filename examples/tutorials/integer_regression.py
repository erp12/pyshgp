import logging
import random

import numpy as np
from pyshgp.gp.selection import Lexicase
from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet


def target_function(a, b):
    return (2 * a * b) + (b * b)


X = np.arange(50).reshape(-1, 2)
y = np.array([[target_function(x[0], x[1])] for x in X])

instruction_set = (
    InstructionSet()
    .register_by_type(["int"], exclude=["str", "exec", "code"])
    .register_n_inputs(X.shape[1])
)

spawner = GeneSpawner(
    instruction_set=instruction_set,
    literals=[],
    erc_generators=[
        lambda: random.randint(0, 10),
    ]
)


ep_lex_sel = Lexicase(epsilon=True)


est = PushEstimator(
    population_size=200,
    max_generations=50,
    spawner=spawner,
    selector=ep_lex_sel,
    verbose=1
)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    est.fit(X=X, y=y)
    print(est._result.program)
    print(est.predict(X))
    print(est.score(X, y))
