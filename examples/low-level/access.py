from random import randint, shuffle

from pyshgp.utils import PushVector
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.gp.evolvers import SimplePushGPEvolver
from pyshgp.gp.variation import (UniformMutation, Alternation,
                                 VariationOperatorPipeline)


def generate_case():
    length = randint(1, 50)
    arr = list(range(length))
    shuffle(arr)
    i = randint(0, length-1)
    return (PushVector(arr, int), i, arr[i])


training_set = [generate_case() for i in range(30)]


def error_function(program):
    errors = []
    for case in training_set:
        interp = PushInterpreter()
        output = interp.run(program, [case[0], case[1]], ['_integer'])[0]
        if output is None:
            errors.append(1e5)
        elif output == case[2]:
            errors.append(0)
        else:
            errors.append(1)
    return errors


mut = UniformMutation(rate=0.01)
alt = Alternation(rate=0.01, alignment_deviation=10)
ops = [(alt, 0.2), (mut, 0.3), (VariationOperatorPipeline((mut, alt)), 0.5)]


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1, operators=ops,
                              initial_max_genome_size=300,
                              population_size=500, max_generations=300,
                              simplification_steps=5000)
    evo.fit(error_function, 2, ['_integer'])
