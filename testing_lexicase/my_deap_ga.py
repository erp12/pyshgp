# -*- coding: utf-8 -*-
"""
Created on Sun May 22 16:22:04 2016

@author: Eddie
"""
import random
from deap import base, creator, tools

import pysh_tools

#########
# TYPES #
#########

# Create a type called FitnessMin that has a base class of base.Fitness,
# and has weights of -1 to specify fitness should be minimized.
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# Create a type called Individual, that is a list, 
# and has a fitness of type FitnessMin.
creator.create("Individual", list, fitness=creator.FitnessMin)

##################
# INITIALIZATION #
##################

# Size of genome
IND_SIZE = 20

# Create a toolbox for evolution that contains the evolutionary operators
toolbox = base.Toolbox()
# Register "initial_gene_val" as a function returning a radom float value
toolbox.register("initial_gene_val", random.random)
# Make alias "individual" for the tools.initRepeat function with arguments that
# construct "Individual" type of n genes with initial values from initial_gene_val.
toolbox.register("produce_individual", tools.initRepeat, creator.Individual,
                 toolbox.initial_gene_val, n=IND_SIZE)                
# Make alias "population" for the tools.initRepeat functiuon with arguments that
# construct a list of calls to "individual"
toolbox.register("population", tools.initRepeat, list, toolbox.produce_individual)

#############
# Operators #
#############

# Define the evaluate function
def evaluate(individual):
    return abs(sum(individual)),

# Register "mate" as two point crossover, implemented as part of DEAP
toolbox.register("mate", tools.cxTwoPoint)
# Register "mutate" as Gausian mutation, implemented as part of DEAP
toolbox.register("mutate", tools.mutGaussian, mu=0, sigma=1, indpb=0.1)
# Register "select" as tournament sections, implemented as part of DEAP
#toolbox.register("select", tools.selTournament, tournsize=3)
# Register "evaluate" as the evaluate function
toolbox.register("evaluate", evaluate)

toolbox.register("select", pysh_tools.lexicase_selection)

################
# GA Algorithm #
################
def main():
    # Create a populatiuon of size 50
    pop = toolbox.population(n=100)
    # Define probabilities of operators, and number of generations
    CXPB, MUTPB, NGEN = 0.5, 0.2, 100

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    # Assign fitnesses to inidividuals in population
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    # for each generation g
    for g in range(NGEN):
        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = list(map(toolbox.evaluate, invalid_ind))
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # The population is entirely replaced by the offspring
        pop[:] = offspring

    return pop

final_population = sorted(main(), key=evaluate)
best = final_population[0]
worst = final_population[-1]
print( "Best Genome", best )
print( "Evaluation of Best:", evaluate(best) )
print( "Evaluation of Worst:", evaluate(worst) )