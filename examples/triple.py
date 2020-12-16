import numpy as np
import random

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner

"""
In this demo, we attempt to evolve a program that triples each number in a given data set.
This is a basic example that has been simplified as much as possible.
"""

"""
To start, we must define our problem by creating two data sets of example input-output pairs.
One will be used for training, and the other will be used to test our program on unseen data.
To get the true output for the data sets, we will manually write a `target_function` function.
For example, if the input data set 'X' was [1,-12,4,0], the output 'y' would be [3,-36,12,0]
"""


# used to get correct output values
def target_function(i):
    return i * 3


# training data set; X is input, y is target output
X = np.arange(-15, 15).reshape(-1, 1)
y = [[target_function(x)] for x in X]

# testing data set; testX is input, testy is output
testX = np.arange(0, 30).reshape(-1, 1)
testy = [[target_function(tx)] for tx in testX]

"""
Next we have to declare our `GeneSpawner`. 
A spawner holds all the instructions, literals, erc generators, 
and inputs that we want to appear in our genomes/programs.
It will be used by evolution to generate random genomes for our initial population and random genes for mutation.
A spawner has many parameters that can be filled and changed, 
but here we make use of as many of the default values as possible and filled in only what is necessary.
"""

spawner = GeneSpawner(
    n_inputs=1,
    instruction_set="core",
    literals=[],
    erc_generators=[lambda: random.randint(0, 10)]
)

"""
We now have everything we need to configure a run of PushGP.
We will create a `PushEstimator` and parameterize it however we want. 
Let's be sure to pass an instance of our spawner.
Like earlier, we  simplified the estimator by only passing it what is necessary,
    but there are several other parameters that can be filled and changed.
"""

if __name__ == "__main__":
    est = PushEstimator(
        spawner=spawner,
        simplification_steps=2000,
        parallelism=False,
        verbose=2
    )

    """
    Now we begin our PushGP run!
    We will call the estimator's `.fit` method on our training data. 
    This function evolves and finds the best program that solves the given problem (tripling the numbers in 'X').
    This  function also prints a lot of information as it evolves and runs. You can ignore most of this for now. 
    After it prints "End Run," it will state whether or not a solution was found.      
    """

    est.fit(X=X, y=y)
    print()

    """
    Next we print the push program using '.solution.program.pretty_str().'
    This will print out a String of push commands that make up the program. 
    If no solution was found, it will print the best program it found instead.
    """

    print("Best program found:")
    print(est.solution.program.pretty_str())

    """
    Lastly, we call '.score' on our test data. 
    If the test errors in the array are all zero, we found a generalizing solution!
    """

    print("Test errors:")
    print(est.score(testX, testy))

