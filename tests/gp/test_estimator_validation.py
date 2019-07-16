import numpy as np
import random
from math import pow, sqrt
from functools import partial

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.atoms import CodeBlock


def run_ga_on_odd_test(parallelism):
    X = np.arange(-10, 10).reshape(-1, 1)
    y = [[bool(x[0] % 2)] for x in X]

    instruction_set = (
        InstructionSet()
        .register_core_by_stack({"int"}, exclude_stacks={"str", "exec", "code"})
        .register_n_inputs(X.shape[1])
    )

    spawner = GeneSpawner(
        instruction_set=instruction_set,
        literals=[],
        erc_generators=[
            partial(random.randint, 0, 10),
        ]
    )

    est = PushEstimator(
        spawner=spawner,
        population_size=40,
        max_generations=10,
        simplification_steps=2,
        parallelism=parallelism)
    est.fit(X, y)

    assert isinstance(est._result.program, CodeBlock)
    assert len(est._result.program) > 0


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
        instruction_set=point_instr_set,
        literals=[],
        erc_generators=[]
    )

    est = PushEstimator(
        spawner=spawner,
        population_size=40,
        max_generations=10,
        simplification_steps=2,
        interpreter=PushInterpreter(point_instr_set),
    )
    est.fit(X, y)

    assert isinstance(est._result.program, CodeBlock)
    assert len(est._result.program) > 0
