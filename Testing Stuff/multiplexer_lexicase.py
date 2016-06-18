import random
import operator
import csv

import numpy

from scoop import futures

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import pysh_tools

def if_then_else(condition, out1, out2):
    return out1 if condition else out2

# Initialize Multiplexer problem input and output vectors

MUX_SELECT_LINES = 3
MUX_IN_LINES = 2 ** MUX_SELECT_LINES
MUX_TOTAL_LINES = MUX_SELECT_LINES + MUX_IN_LINES

# input : [A0 A1 A2 D0 D1 D2 D3 D4 D5 D6 D7] for a 8-3 mux
inputs = [[0] * MUX_TOTAL_LINES for i in range(2 ** MUX_TOTAL_LINES)]
outputs = [None] * (2 ** MUX_TOTAL_LINES)

for i in range(2 ** MUX_TOTAL_LINES):
    value = i
    divisor = 2 ** MUX_TOTAL_LINES
    # Fill the input bits
    for j in range(MUX_TOTAL_LINES):
        divisor /= 2
        if value >= divisor:
            inputs[i][j] = 1
            value -= divisor
    
    # Determine the corresponding output
    indexOutput = MUX_SELECT_LINES
    for j, k in enumerate(inputs[i][:MUX_SELECT_LINES]):
        indexOutput += k * 2**j
    outputs[i] = inputs[i][indexOutput]

pset = gp.PrimitiveSet("MAIN", MUX_TOTAL_LINES, "IN")
pset.addPrimitive(operator.and_, 2)
pset.addPrimitive(operator.or_, 2)
pset.addPrimitive(operator.not_, 1)
pset.addPrimitive(if_then_else, 3)
pset.addTerminal(1)
pset.addTerminal(0)

creator.create("FitnessMax", base.Fitness, weights=(1.0,)*len(outputs))
creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("map", futures.map)
toolbox.register("expr", gp.genFull, pset=pset, min_=2, max_=4)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("compile", gp.compile, pset=pset)

def evalMultiplexer(individual):
    #print('|')
    func = toolbox.compile(expr=individual)
    case_bools = list(func(*in_) == out for in_, out in zip(inputs, outputs))
    return [ int(x) for x in case_bools ]

toolbox.register("evaluate", evalMultiplexer)
toolbox.register("select", pysh_tools.lexicase_selection)
toolbox.register("mate", gp.cxOnePoint)
toolbox.register("expr_mut", gp.genGrow, min_=0, max_=2)
toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

def main():
    # random.seed(10)
    # logbook = tools.Logbook()

    pop = toolbox.population(n=20)
    hof = tools.HallOfFame(1)
    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", lambda fit: numpy.mean(numpy.mean(fit, axis = 0)))
    stats.register("std", lambda fit: numpy.std(numpy.mean(fit, axis = 0)))
    stats.register("min", lambda fit: numpy.min(numpy.mean(fit, axis = 0)))
    stats.register("max", lambda fit: numpy.max(numpy.mean(fit, axis = 0)))
    
    result = algorithms.eaSimple(pop, toolbox, 0.8, 0.1, 50, stats, halloffame=hof)
    best_population = result[0]
    logbook = result[1]

    with open('multiplexer_lexicase_log.csv', 'w') as csvfile:
        fieldnames = ['nevals', 'gen', 'avg', 'std', 'min', 'max']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in logbook:
            writer.writerow(row)

    return pop, stats, hof

if __name__ == "__main__":
    main()
