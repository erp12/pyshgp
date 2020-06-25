import numpy as np

from pyshgp.gp.estimators import PushEstimator
from pyshgp.gp.genome import GeneSpawner
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.instruction_set import InstructionSet
from pyshgp.push.instruction import SimpleInstruction
from pyshgp.push.type_library import PushTypeLibrary
from pyshgp.push.types import PushFloat

"""
In this demo, we attempt to evolve a program that can find the difference between the areas of two rectangles.
This is a demonstration of how to create your own PushTypes and PushInstructions.
"""

"""
We begin by creating a Rectangle class. 
Each Rectangle has an float width and height.
This class will be the underlying type for our custom PushType.
"""


class Rectangle:

    # constructor
    def __init__(self, height: float, width: float):
        self.height = height
        self.width = width

    # checks the equality of two Rectangle objects
    def __eq__(self, other):
        if isinstance(other, Rectangle):
            return self.height == other.height and self.width == other.width
        return False

    # returns the Rectangle object's representation
    def __repr__(self):
        return "Rectangle: {height} X {width}".format(height=self.height, width=self.width)


"""
Next, we create a function to converts something into a Rectangle if possible.
This function will be the coercion function for our custom PushType.
"""


def to_rect(thing):
    return Rectangle(float(thing[0]), float(thing[1]))


"""
Next, we create the target function we would like to synthesize.
Our target function returns the difference in area between two rectangles.
This is also the function used to define of one of our custom instructions.
"""


def area_difference(r1, r2):
    area_1 = r1.height * r1.width
    area_2 = r2.height * r2.width
    return (area_1 - area_2),  # comma at the end packages return value into a tuple


"""
Now we create another function used to define of one of our custom instructions.
This function returns a tuple containing a rectangle made from two floats.
"""


def rectangle_from_floats(i1, i2):
    return Rectangle(i1, i2),  # comma at the end packages return value into a tuple


"""
Next, we define our custom instructions that manipulate rectangles by defining parameters in SimpleInstruction.
We want rectangle_areas_instruction to find difference in area between two rectangles, and push it to the float stack.
We want rectangle_from_floats_instruction to take two floats and push a rectangle.
"""

rectangle_areas_instruction = SimpleInstruction(
    name="rectangle_area_diff",  # unique name for the instruction
    f=area_difference,  # function whose signature matches input_stacks and output_stacks
    input_stacks=["rectangle", "rectangle"],  # list of PushType names to use when popping arguments from PushState
    output_stacks=["float"],  # list of PushType names to use when pushing function results to the PushState
    code_blocks=0  # number of CodeBlocks to open following the instruction in a Genome
)

rectangle_from_floats_instruction = SimpleInstruction(
    name="rectangle_from_floats", f=rectangle_from_floats,
    input_stacks=["float", "float"], output_stacks=["rectangle"], code_blocks=0
)

"""
Now we must define our problem by creating two data sets of example input-output pairs.
One will be used for training, and the other will be used to test our program on unseen data.
To get the true output for the data sets, we will use the "target_function" function.
"""

X = [[Rectangle(row[0], row[1]), Rectangle(row[2], row[3])] for row in np.random.rand(20, 4)]
y = [[area_difference(r[0], r[1])] for r in X]

"""
Next, we create a type library that specifies we will be synthesizing programs that manipulate 
    "floats" (built-in to pyshgp) and "rectangles" (custom for this problem).
"""

type_library = (
    PushTypeLibrary(register_core=False)
        .register(PushFloat)
        .create_and_register(name="rectangle", underlying_types=(Rectangle,), coercion_func=to_rect)
)

"""
Next we define out instruction set using the type library and the two instructions we created.
Our two custom instructions as well as the input instructions are  defined.
The instruction set will register all core instructions that can be supported 
    using only exec, code, float, and rectangle types because the only core PushType we registered was "PushInt"
For example, the instruction int_from_float will NOT be registered because
    our type library does not define a type that would support the "int" stack.
"""

instruction_set = (
    InstructionSet(type_library=type_library, register_core=True)
        .register(rectangle_areas_instruction)
        .register(rectangle_from_floats_instruction)
)

print("Stacks: ", instruction_set.required_stacks())
print("Types: ", type_library.supported_stacks())
print("Instruction Set: ", instruction_set.keys())
print()

"""
Next we have to declare our "GeneSpawner."
We pass to it our instruction_set.
n_inputs=2 because we would like the genome to possibly include 2 input instructions.
literals=[2.0] because it will detect that 2.0 is a float, 
    and the spawner will pull floats when spawning genes and genomes.

"""

spawner = GeneSpawner(
    n_inputs=2,
    instruction_set=instruction_set,
    literals=[2.0],
    erc_generators=[]
)

"""
We have everything we need to configure a run of PushGP.
We will create a "PushEstimator" and parameterize it however we want. 
We pass an instance of our spawner and define a custom interpreter 
"""

est = PushEstimator(
    spawner=spawner,
    population_size=300,
    max_generations=20,
    initial_genome_size=(5, 55),
    simplification_steps=500,
    interpreter=PushInterpreter(instruction_set),
    verbose=2
)

"""
Now we begin our PyshGP run with custom instructions and types.
If we do find a solution, it should happen relatively quickly. 
Otherwise, the run may have gotten "stuck" or not find a solution during the evolutionary process. 
    We have set max_generations=20 to account for this. Try running it again if this happens.
"""

if __name__ == "__main__":
    est.fit(X, y)
    print()
    print("Best program found:")
    print(est.solution.program.pretty_str())
    print()
    print("Errors:")
    print(est.score(X, y))
