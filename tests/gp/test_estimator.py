import os

import numpy as np
import pandas as pd
import random

import pytest
from math import pow, sqrt
from functools import partial

from pyshgp.gp.individual import Individual

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet


@pytest.fixture
def simple_test_spawner():
    instruction_set = InstructionSet().register_core_by_stack({"int"}, exclude_stacks={"str", "exec", "code"})
    spawner = GeneSpawner(
        n_inputs=1,
        instruction_set=instruction_set,
        literals=[],
        erc_generators=[
            partial(random.randint, 0, 10),
        ]
    )
    return spawner


def run_ga_on_odd_test(spawner, parallelism):
    X = np.arange(-10, 10).reshape(-1, 1)
    y = [[bool(x[0] % 2)] for x in X]

    est = PushEstimator(
        spawner=spawner,
        population_size=10,
        max_generations=3,
        simplification_steps=3,
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


def test_ga(simple_test_spawner):
    run_ga_on_odd_test(simple_test_spawner, False)
    run_ga_on_odd_test(simple_test_spawner, True)
    run_ga_on_odd_test(simple_test_spawner, 2)


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
        population_size=10,
        max_generations=3,
        simplification_steps=3,
        interpreter=PushInterpreter(point_instr_set),
    )
    est.fit(X, y)

    assert isinstance(est.solution, Individual)
    assert len(est.solution.program.code) > 0


def test_estimator_with_pandas(simple_test_spawner):
    df = pd.DataFrame({
        "x1": [-2, -1, 0, 1, 2],
        "x2": [-1, 2, -3, 4, -5],
        "y":  [2, -2, 0, 4, -10]
    })

    est = PushEstimator(
        spawner=simple_test_spawner,
        population_size=10,
        max_generations=3,
        simplification_steps=3,
        parallelism=False
    )
    est.fit(df[["x1", "x2"]], df[["y"]])

    assert isinstance(est.solution, Individual)
    assert len(est.solution.program.code) > 0
