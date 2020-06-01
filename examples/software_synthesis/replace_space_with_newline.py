"""Replace Space With Newline.

Problem Source: iJava (http://ijava.cs.umass.edu/)

Given a string input, print the string, replacing spaces with newlines.
The input string will not have tabs or newlines, but may have multiple spaces
in a row. It will have maximum length of 20 characters. Also, the program
should return the integer count of the non-whitespace characters.
"""
from random import random, randint, choice
import numpy as np
import time
import string

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.types import Char


def target_function(s: str):
    """Generate a training data point."""
    return [
        s.replace(" ", "\n"),
        len(s) - s.count(' ')
    ]


_possible_chars = string.ascii_letters + string.digits + string.punctuation


def synthetic_input():
    """Generate a string to use as input to a trining data point."""
    size = randint(0, 19) + 2
    s = ""
    for ndx in range(size):
        if random() < 0.2:
            s += " "
        else:
            s += choice(_possible_chars)
    return s


# Datasets

X_train_edge = [
    [""],
    ["A"],
    ["*"],
    [" "],
    ["s"],
    ["B "],
    ["  "],
    [" D"],
    ["ef"],
    ["!!"],
    [" F "],
    ["T L"],
    ["4ps"],
    ["q  "],
    ["   "],
    ["  e"],
    ["hi "],
    ["  $  "],
    ["      9"],
    ["i !" * 4 + "i"],
    ["8" * 20],
    [" " * 20],
    ["s" * 20],
    ["1 " * 10],
    [" v" * 10],
    ["Ha " * 5],
    ["x y!" * 5],
    ["G5" * 10],
    [">_=]" * 5],
    ["^_^ " * 5],
]
y_train_edge = [target_function(x[0]) for x in X_train_edge]

X_train_synthetic = [[synthetic_input()] for _ in range(70)]
y_train_synthetic = [target_function(x[0]) for x in X_train_synthetic]

X_train = X_train_edge + X_train_synthetic
y_train = y_train_edge + y_train_synthetic

X_test = [[synthetic_input()] for _ in range(100)]
y_test = [target_function(x[0]) for x in X_test]


# Spawner

def random_char():
    """Return a random character."""
    return Char(choice(_possible_chars))


spawner = GeneSpawner(
    n_inputs=1,
    instruction_set=InstructionSet().register_core_by_stack({"int", "bool", "string", "char", "exec", "stdout"}),
    literals=[" ", "\n"],
    erc_generators=[
        random_char,
    ],
)

if __name__ == "__main__":
    est = PushEstimator(
        search="GA",
        population_size=500,
        max_generations=150,
        spawner=spawner,
        simplification_steps=100,
        last_str_from_stdout=True,
        parallelism=True,
        verbose=2
    )

    start = time.time()
    est.fit(X=X_train, y=y_train)
    end = time.time()
    print("train_error: ", est.solution.total_error)
    print("test_error: ", np.sum(est.score(X_test, y_test)))
    print("runtime: ", end - start)
    print("final_generation: ", est.search.generation)
    print("best_genome: ", est.solution.genome)
