import numpy as np
from pyshgp.gp.estimators import PushEstimator
from pyshgp.push.atoms import CodeBlock


def test_ga_on_odd():
    X = np.arange(-10, 10).reshape(-1, 1)
    y = [bool(x % 2) for x in X]

    est = PushEstimator(population_size=20, max_generations=10, simplification_steps=100)
    est.fit(X, y)

    assert isinstance(est._result.program, CodeBlock)
    assert len(est._result.program) > 0
