import random
import time
import numpy as np

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.types import IntVector


def target_function(v1: IntVector, v2: IntVector):
    return v1 == v2[::-1]


def random_vector():
    size = random.randint(0, 50)
    return IntVector([random.randint(-100, 100) for _ in range(size)])


def mirror_vectors():
    v = random_vector()
    return [v, IntVector(v[::-1])]


def equal_vectors():
    v = random_vector()
    return [v, v]


def random_vectors():
    return [random_vector(), random_vector()]


X_train_edge = [
    [IntVector([]), IntVector([])],
    [IntVector([0]), IntVector([1])],
    [IntVector([1]), IntVector([0])],
    [IntVector([1]), IntVector([1])],
    [IntVector([16]), IntVector([-44])],
    [IntVector([-12]), IntVector([-13])],
    [IntVector([1, 2]), IntVector([2, 1])],
    [IntVector([1, 1]), IntVector([0, 1])],
    [IntVector([7, 0]), IntVector([0, 7])],
    [IntVector([5, 8]), IntVector([5, 8])],
    [IntVector([34, 12]), IntVector([34, 12])],
    [IntVector([456, 456]), IntVector([456, 456])],
    [IntVector([-431, -680]), IntVector([40, 831])],
    [IntVector([1, 2, 1]), IntVector([1, 2, 1])],
    [IntVector([1, 2, 3, 4, 5, 4, 3, 2, 1]), IntVector([1, 2, 3, 4, 5, 4, 3, 2, 1])],
    [IntVector([45, 99, 0, 12, 44, 7, 7, 44, 12, 0, 99, 45]), IntVector([45, 99, 0, 12, 44, 7, 7, 44, 12, 0, 99, 45])],
    [IntVector([33, 45, -941]), IntVector([33, 45, -941])],
    [IntVector([33, 45, -941]), IntVector([45, -941, 33])],
    [IntVector([33, 45, -941]), IntVector([-941, 33, 45])],
    [IntVector([33, 45, -941]), IntVector([33, -941, 45])],
    [IntVector([33, 45, -941]), IntVector([45, 33, -941])],
    [IntVector([33, 45, -941]), IntVector([-941, 45, 33])],
]

X_train_synthetic = [mirror_vectors() for _ in range(10)] + \
                    [equal_vectors() for _ in range(10)] + \
                    [random_vectors() for _ in range(10)]

X_train = X_train_edge + X_train_synthetic
y_train = [[target_function(x[0], x[1])] for x in X_train]


X_test = [mirror_vectors() for _ in range(100)] + \
         [equal_vectors() for _ in range(100)] + \
         [random_vectors() for _ in range(100)]
y_test = [[target_function(x[0], x[1])] for x in X_test]


spawner = GeneSpawner(
    n_inputs=2,
    instruction_set=InstructionSet().register_core_by_stack({"int", "bool", "vector_int", "exec"}),
    literals=[" ", "\n"],
    erc_generators=[
        lambda: random.random() < 0.5,
    ],
)


if __name__ == "__main__":
    est = PushEstimator(
        search="GA",
        population_size=500,
        max_generations=150,
        spawner=spawner,
        simplification_steps=100,
        verbose=2
    )

    start = time.time()
    est.fit(X=X_train, y=y_train)
    end = time.time()
    print("========================================")
    print("post-evolution stats")
    print("========================================")
    print("Runtime: ", end - start)
    print("Test Error: ", np.sum(est.score(X_test, y_test)))
