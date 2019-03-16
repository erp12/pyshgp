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
import logging
import sys

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.types import Char


def target_function(s: str):
    return [
        s.replace(" ", "\n"),
        len(s) - s.count(' ')
    ]


_possible_chars = string.ascii_letters + string.digits + string.punctuation


def synthetic_input():
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

instruction_set = (
    InstructionSet()
    .register_by_type(["int", "bool", "string", "char", "exec", "stdout"])
    .register_n_inputs(1)
)

spawner = GeneSpawner(
    instruction_set=instruction_set,
    literals=[Char(" "), Char("\n")],
    erc_generators=[
        lambda: Char(choice(_possible_chars)),
        synthetic_input
    ],
)

# Estimator

est = PushEstimator(
    search="GA",
    population_size=1000,
    max_generations=100,
    spawner=spawner,
    last_str_from_stdout=True,
    verbose=2
)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stdout
    )
    start = time.time()
    est.fit(X=X_train, y=y_train)
    end = time.time()
    print("train_error: ", est.search.best_seen.total_error)
    print("test_error: ", np.sum(est.score(X_test, y_test)))
    print("runtime: ", end - start)
    print("final_generation: ", est.search.generation)
    print("best_genome_json: ", est.search.best_seen.genome.jsonify())
