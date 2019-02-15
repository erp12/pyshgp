"""The **string_demo** problem is a simple benchmark that is designed to
deomonstrate a PushGP's string manipulation capabilities. The goal of the
problem is as follows:

Take the input string, remove the last 2 characters, and then concat this
result with itself.

By default, the error function will be the Damerau-Levenshtein Distance.
"""
import numpy as np
import random

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet


def target_function(s):
    return s[:-2] + s[:-2]


X = np.array([
    "abcde", "", "E", "Hi", "Tom", "leprechaun", "zoomzoomzoom",
    "qwertyuiopasd", "GallopTrotCanter", "Quinona", "_abc"
]).reshape(-1, 1)
y = np.array([target_function(s[0]) for s in X])


instruction_set = (
    InstructionSet()
    .register_by_type(["str", "int"])
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
    search="SA",
    max_generations=5000,
    spawner=spawner
)

if __name__ == "__main__":
    est.fit(X=X, y=y, verbose=False)
    print(est._result.program)
    print(est.predict(X))
    print(est.score(X, y))
