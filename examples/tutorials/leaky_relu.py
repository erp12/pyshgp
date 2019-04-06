"""The ReLU function is a common activation function used in artifical neural netoworks.

```
relu(x) = max(0, x)
```

The Leaky ReLU function is a varient of the ReLU function designed to avoid
having nodes "die". Its definition is as follows.

```
leaky_relu(x) = max(0.1x, x)
```

This problem attempts to synthesize a program that compute the output of both
the ReLU and LeakyReLU functions.

"""
import logging
import numpy as np
import random
import sys

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.gp.selection import Lexicase
from pyshgp.push.instruction_set import InstructionSet


def target_function(x: float) -> (float, float):
    """Generate a training data point."""
    return (max(0.0, x), max(0.1 * x, x))


X = np.arange(-1.0, 1.0, 0.15).reshape([-1, 1])
y = np.array([target_function(x[0]) for x in X])

instruction_set = (
    InstructionSet()
    .register_core_by_stack({"float", "bool"})
    .register_n_inputs(X.shape[1])
)


spawner = GeneSpawner(
    instruction_set=instruction_set,
    literals=[0.1, 0.0],
    erc_generators=[
        lambda: random.randint(0, 10),
    ]
)


ep_lex_sel = Lexicase(epsilon=True)


est = PushEstimator(
    population_size=500,
    max_generations=50,
    spawner=spawner,
    selector=ep_lex_sel,
    verbose=2
)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stdout
    )
    est.fit(X=X, y=y)
    print(est._result.program)
    print(est.predict(X))
    print(est.score(X, y))
