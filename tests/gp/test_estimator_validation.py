import numpy as np
import random

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.atoms import CodeBlock


def test_ga_on_odd():
    X = np.arange(-10, 10).reshape(-1, 1)
    y = [bool(x % 2) for x in X]

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

    est = PushEstimator(
        spawner=spawner,
        population_size=20,
        max_generations=10,
        simplification_steps=100)
    est.fit(X, y)

    assert isinstance(est._result.program, CodeBlock)
    assert len(est._result.program) > 0
