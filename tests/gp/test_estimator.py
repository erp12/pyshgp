import os

import numpy as np
import random
from math import pow, sqrt
from functools import partial

from pyshgp.gp.individual import Individual

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet


def run_ga_on_odd_test(parallelism):
    X = np.arange(-10, 10).reshape(-1, 1)
    y = [[bool(x[0] % 2)] for x in X]

    instruction_set = (
        InstructionSet()
        .register_core_by_stack({"int"}, exclude_stacks={"str", "exec", "code"})
    )

    spawner = GeneSpawner(
        n_inputs=1,
        instruction_set=instruction_set,
        literals=[],
        erc_generators=[
            partial(random.randint, 0, 10),
        ]
    )

    est = PushEstimator(
        spawner=spawner,
        population_size=30,
        max_generations=3,
        simplification_steps=10,
        parallelism=parallelism)
    est.fit(X, y)

    assert isinstance(est.solution, Individual)
    assert len(est.solution.program.code) > 0

    path = "tmp.push"
    solution = est.solution.copy(deep=True)
    est.save(path)
    est.load(path)
    assert solution == est.solution
    os.remove(path)


def test_ga():
    run_ga_on_odd_test(False)
    run_ga_on_odd_test(True)
    run_ga_on_odd_test(2)


def point_distance(p1, p2):
    delta_x = p2.x - p1.x
    delta_y = p2.y - p1.y
    return sqrt(pow(delta_x, 2.0) + pow(delta_y, 2.0))


def test_estimator_with_custom_types(point_cls, point_instr_set):
    X = np.arange(-1.0, 1.0, 0.05).reshape(-1, 4)
    y = [[point_distance(point_cls(x[0], x[1]), point_cls(x[2], x[3]))] for x in X]

    spawner = GeneSpawner(
        n_inputs=1,
        instruction_set=point_instr_set,
        literals=[],
        erc_generators=[]
    )

    est = PushEstimator(
        spawner=spawner,
        population_size=30,
        max_generations=3,
        simplification_steps=2,
        interpreter=PushInterpreter(point_instr_set),
    )
    est.fit(X, y)

    assert isinstance(est.solution, Individual)
    assert len(est.solution.program.code) > 0
