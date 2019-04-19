"""The point distance problem.

The goal of this example is to evolve a program that computes the distance
between two x-y points. This is acomplished by using a custom PushType and
a custom PushInstruction.
"""
import logging
import numpy as np
import sys
from math import pow, sqrt


from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.instruction import SimpleInstruction
from pyshgp.push.type_library import PushTypeLibrary
from pyshgp.push.types import PushFloat


class Point:
    """A point on a 2D x-y plane."""

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False

    def __repr__(self):
        return "Point<{x},{y}>".format(x=self.x, y=self.y)


def to_point(thing):
    """Convert thing into a Point if possible."""
    return Point(float(thing[0]), float(thing[1]))


# The target funcgtion we would like to sythesize.
# Also the function used to define of one of our custom instructions.
def point_distance(p1, p2):
    """Return the distance between two points."""
    delta_x = p2.x - p1.x
    delta_y = p2.y - p1.y
    return sqrt(pow(delta_x, 2.0) + pow(delta_y, 2.0)),


# Another function used to define of one of our custom instructions.
def point_from_floats(f1, f2):
    """Return a tuple containint a Point made from two floats."""
    return Point(f1, f2),


# Our custom instructions objects that manipulate points.
point_distance_insrt = SimpleInstruction(
    "point_dist", point_distance,
    ["point", "point"], ["float"], 0
)
point_from_floats_instr = SimpleInstruction(
    "point_from_floats", point_from_floats,
    ["float", "float"], ["point"], 0
)


# Training data
X = [[Point(row[0], row[1]), Point(row[2], row[3])] for row in np.random.rand(20, 4)]
y = [[point_distance(x[0], x[1])] for x in X]


# Custom type library that specifies we will be sythesizing programs that
# manipulate "floats" (built-in to pyshgp) and "points" (custom for this problem)
type_library = (
    PushTypeLibrary(register_core=False)
    .register(PushFloat)
    .create_and_register("point", (Point, ), coercion_func=to_point)
)


# An instruction set which will regiser all core instructions that can be supported
# using only exec, code, stdout, float, and point types.
#
# For example, the instruction int_from_float will NOT be registerd because
# our type library does not define a type that would support the "int" stack.
#
# Our two custom instructions as well as the input instructions are also defined.
instruction_set = (
    InstructionSet(type_library=type_library, register_core=True)
    .register(point_distance_insrt)
    .register(point_from_floats_instr)
    .register_n_inputs(2)
)

print(instruction_set.keys())

spawner = GeneSpawner(
    instruction_set=instruction_set,
    literals=[2.0],
    erc_generators=[]
)


# Our estimator with a custom interpreter defined.
est = PushEstimator(
    spawner=spawner,
    population_size=500,
    max_generations=20,
    simplification_steps=1000,
    interpreter=PushInterpreter(instruction_set),
    verbose=2
)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        stream=sys.stdout
    )
    est.fit(X, y)
    print(est._result.program)
    print(est.predict(X))
    print(est.score(X, y))
