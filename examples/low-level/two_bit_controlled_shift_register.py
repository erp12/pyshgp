from pyshgp.utils import merge_sets
from pyshgp.push.interpreter import PushInterpreter
from pyshgp.push.registered_instructions import get_instructions_by_pysh_type
from pyshgp.gp.evolvers import SimplePushGPEvolver
from pyshgp.gp.variation import (UniformMutation, Alternation,
                                 VariationOperatorPipeline)


cases = [(0, 0, 0),
         (0, 0, 1),
         (0, 1, 0),
         (0, 1, 1),
         (1, 0, 0),
         (1, 0, 1),
         (1, 1, 0),
         (1, 1, 1)]


def two_bit_control_shift(a, b, c):
    if a:
        return (a, c, b)
    else:
        return (a, b, c)


def error_function(program):
    errors = []
    for case in cases:
        interpreter = PushInterpreter()
        outputs = interpreter.run(program, case, ['_boolean', '_boolean', '_boolean'])
        targets = two_bit_control_shift(case)
        e = 0

        if outputs[0] is None:
            e += 1e4
        elif outputs[0] != targets[0]:
            e += 1

        if outputs[1] is None:
            e += 1e4
        elif outputs[1] != targets[1]:
            e += 1

        if outputs[2] is None:
            e += 1e4
        elif outputs[2] != targets[2]:
            e += 1

        errors.append(e)
    return errors


atom_generators = list(merge_sets(get_instructions_by_pysh_type('_boolean'),
                                  get_instructions_by_pysh_type('_exec')))
mut = UniformMutation(rate=0.1)
alt = Alternation(rate=0.1, alignment_deviation=10)
ops = [(alt, 0.2), (mut, 0.3), (VariationOperatorPipeline((mut, alt)), 0.5)]


if __name__ == "__main__":
    evo = SimplePushGPEvolver(n_jobs=-1, verbose=1, operators=ops,
                              atom_generators=atom_generators,
                              initial_max_genome_size=300,
                              population_size=500, max_generations=300,
                              simplification_steps=5000)
    evo.fit(error_function, 3, ['_boolean', '_boolean', '_boolean'])
