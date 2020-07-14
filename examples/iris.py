import random

import pandas as pd
from pyshgp.push.instruction_set import InstructionSet

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner


# A sample of the famous Iris dataset.
data = pd.DataFrame(
    data=[
        [5.1, 3.5, 1.4, 0.2, 0],
        [4.9, 3.0, 1.4, 0.2, 0],
        [4.7, 3.2, 1.3, 0.2, 0],
        [4.6, 3.1, 1.5, 0.2, 0],
        [5.0, 3.6, 1.4, 0.2, 0],
        [5.4, 3.9, 1.7, 0.4, 0],
        [4.6, 3.4, 1.4, 0.3, 0],
        [5.0, 3.4, 1.5, 0.2, 0],
        [4.4, 2.9, 1.4, 0.2, 0],
        [4.9, 3.1, 1.5, 0.1, 0],
        [7.0, 3.2, 4.7, 1.4, 1],
        [6.4, 3.2, 4.5, 1.5, 1],
        [6.9, 3.1, 4.9, 1.5, 1],
        [5.5, 2.3, 4.0, 1.3, 1],
        [6.5, 2.8, 4.6, 1.5, 1],
        [5.7, 2.8, 4.5, 1.3, 1],
        [6.3, 3.3, 4.7, 1.6, 1],
        [4.9, 2.4, 3.3, 1.0, 1],
        [6.6, 2.9, 4.6, 1.3, 1],
        [5.2, 2.7, 3.9, 1.4, 1],
        [6.3, 3.3, 6.0, 2.5, 2],
        [5.8, 2.7, 5.1, 1.9, 2],
        [7.1, 3.0, 5.9, 2.1, 2],
        [6.3, 2.9, 5.6, 1.8, 2],
        [6.5, 3.0, 5.8, 2.2, 2],
        [7.6, 3.0, 6.6, 2.1, 2],
        [4.9, 2.5, 4.5, 1.7, 2],
        [7.3, 2.9, 6.3, 1.8, 2],
        [6.7, 2.5, 5.8, 1.8, 2],
        [7.2, 3.6, 6.1, 2.5, 2],
    ],
    columns=["sepal_length", "sepal_width", "petal_length", "petal_width", "label"]
)


spawner = GeneSpawner(
    n_inputs=1,
    instruction_set=InstructionSet().register_core_by_stack({"bool", "int", "float"}),
    literals=[0, 1, 2],
    erc_generators=[
        lambda: random.randint(0, 10),
        random.random
    ]
)


if __name__ == "__main__":
    est = PushEstimator(
        spawner=spawner,
        population_size=300,
        max_generations=100,
        verbose=2
    )

    x = data[["sepal_length", "sepal_width", "petal_length", "petal_width"]]
    y = data[["label"]]

    est.fit(x, y)
