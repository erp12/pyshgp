import numpy as np
import random
from math import pow, sqrt

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.instruction import SimpleInstruction
from pyshgp.push.atoms import CodeBlock
from pyshgp.push.type_library import PushTypeLibrary
from pyshgp.push.types import PushFloat


def test_ga_on_odd():
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
            lambda: random.randint(0, 10),
        ]
    )

    est = PushEstimator(
        spawner=spawner,
        population_size=20,
        max_generations=10,
        simplification_steps=2)
    est.fit(X, y)

    assert isinstance(est._result.program, CodeBlock)
    assert len(est._result.program) > 0


def test_estimator_with_custom_types(point_cls, point_distance_insrt, to_point_func):
    X = np.arange(-1.0, 1.0, 0.05).reshape(-1, 4)
    y = [[point_distance_insrt.f(point_cls(x[0], x[1]), point_cls(x[2], x[3]))] for x in X]

    type_library = (
        PushTypeLibrary(register_core=False)
        .register(PushFloat)
        .create_and_register("point", (point_cls, ), to_point_func)
    )

    print(type_library.keys())

    instruction_set = (
        InstructionSet(type_library=type_library, register_core=True)
        .register(point_distance_insrt)
        .register_n_inputs(X.shape[1])
    )

    print(instruction_set.keys())

    spawner = GeneSpawner(
        instruction_set=instruction_set,
        literals=[],
        erc_generators=[]
    )

    est = PushEstimator(
        spawner=spawner,
        population_size=20,
        max_generations=10,
        simplification_steps=2,
        interpreter=PushInterpreter(instruction_set),
    )
    est.fit(X, y)

    assert isinstance(est._result.program, CodeBlock)
    assert len(est._result.program) > 0
