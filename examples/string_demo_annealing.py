"""The **string_demo** problem solved with simulated annealing.

A simple benchmark that is designed to deomonstrate a PushGP's string manipulation
capabilities. The goal of the problem is as follows:

Take the input string, remove the last 2 characters, and then concat this
result with itself.

By default, the error function will be the Damerau-Levenshtein Distance.

NOTICE: This problem file is run during PyshGP's CI tests as validation tests.
For this reason, the hyperparameters that contribute the most to runtime are kept
artificially low. To see the best search performance, consider increasing
population size, max generations, and initial_genome_size.

"""
import numpy as np
import random

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet


def target_function(s):
    """Generate a training data point."""
    return s[:-2] + s[:-2]


X = np.array([
    "abcde", "", "E", "Hi", "Tom", "leprechaun", "zoomzoomzoom",
    "qwertyuiopasd", "GallopTrotCanter", "Quinona", "_abc"
]).reshape(-1, 1)
y = np.array([[target_function(s[0])] for s in X])


spawner = GeneSpawner(
    n_inputs=1,
    instruction_set=InstructionSet().register_core_by_stack({"str", "int"}),
    literals=[],
    erc_generators=[
        lambda: random.randint(0, 10),
    ]
)


if __name__ == "__main__":
    est = PushEstimator(
        search="SA",
        spawner=spawner,
        max_generations=300,
        initial_genome_size=(10, 50),
        simplification_steps=500,
        parallelism=False,
        verbose=1
    )

    est.fit(X=X, y=y)
    print("Best program found:")
    print(est.solution.program.pretty_str())
    print("Errors:")
    print(est.score(X, y))
