import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

import pysh_tools

IND_INIT_SIZE = 5
MAX_ITEM = 50
MAX_WEIGHT = 50
NBR_ITEMS = 20

# Create the item dictionary: item name is an integer, and value is 
# a (weight, value) 2-uple.
item_set_1 = {0 : (5, 8.1893200425862),
         1 : (4, 1.961792424663205),
         2 : (5, 7.45329877120378),
         3 : (8, 3.8236115324607467),
         4 : (9, 3.198752419455246),
         5 : (4, 5.445358143344826),
         6 : (3, 3.189690419890967),
         7 : (9, 5.431591650068825),
         8 : (7, 4.869171473336515),
         9 : (8, 4.18950030256289),
         10 : (8, 8.04449874168937),
         11 : (1, 1.275744760704853),
         12 : (10, 1.43280905054589),
         13 : (8, 1.246131949503539),
         14 : (7, 4.054753602860906),
         15 : (4, 6.52478274829157),
         16 : (1, 9.7020450746796),
         17 : (4, 2.357690252291086),
         18 : (10, 7.30356881233075),
         19 : (4, 6.11923894013047),
         20 : (3, 3.22361863703772)}

creator.create("Fitness", base.Fitness, weights=(-1.0, 1.0))
creator.create("Individual", set, fitness=creator.Fitness)

toolbox = base.Toolbox()

# Attribute generator
toolbox.register("attr_item", random.randrange, NBR_ITEMS)

# Structure initializers
toolbox.register("individual", tools.initRepeat, creator.Individual, 
    toolbox.attr_item, IND_INIT_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalKnapsack(individual):
    weight = 0.0
    value = 0.0
    for item in individual:
        weight += item_set_1[item][0]
        value += item_set_1[item][1]
    if len(individual) > MAX_ITEM or weight > MAX_WEIGHT:
        return 10000, 0             # Ensure overweighted bags are dominated
    return weight, value

def cxSet(ind1, ind2):
    """Apply a crossover operation on input sets. The first child is the
    intersection of the two sets, the second child is the difference of the
    two sets.
    """
    temp = set(ind1)                # Used in order to keep type
    ind1 &= ind2                    # Intersection (inplace)
    ind2 ^= temp                    # Symmetric Difference (inplace)
    return ind1, ind2
    
def mutSet(individual):
    """Mutation that pops or add an element."""
    if random.random() < 0.5:
        if len(individual) > 0:     # We cannot pop from an empty set
            individual.remove(random.choice(sorted(tuple(individual))))
    else:
        individual.add(random.randrange(NBR_ITEMS))
    return individual,

toolbox.register("evaluate", evalKnapsack)
toolbox.register("mate", cxSet)
toolbox.register("mutate", mutSet)

toolbox.register("select", tools.selNSGA2)
#toolbox.register("select", pysh_tools.lexicase_selection)

def main():
    NGEN = 200
    MU = 50
    LAMBDA = 100
    CXPB = 0.7
    MUTPB = 0.2
    
    pop = toolbox.population(n=100)
    
    # Make a hall of fame
    hof = tools.ParetoFront()
    stats = tools.Statistics(lambda ind: ind.fitness.values)    
    
# DEAP's EVOLUTIONARY LOOP
    algorithms.eaMuPlusLambda(pop, toolbox, MU, LAMBDA, CXPB, MUTPB, NGEN, stats,
                              halloffame=hof)    
    
# MY EVOLUTIONARY LOOP    
#    # for each generation g
#    for g in range(NGEN):
#        print( "Starting Generation", g )
#        #print( len(pop) )
#        
#        # Select the next generation individuals
#        offspring = toolbox.select(pop, len(pop))
#        # Clone the selected individuals
#        offspring = list(map(toolbox.clone, offspring))
#
#        # Apply crossover and mutation on the offspring
#        for child1, child2 in zip(offspring[::2], offspring[1::2]):
#            if random.random() < CXPB:
#                toolbox.mate(child1, child2)
#                del child1.fitness.values
#                del child2.fitness.values
#
#        for mutant in offspring:
#            if random.random() < MUTPB:
#                toolbox.mutate(mutant)
#                del mutant.fitness.values
#
#        # Evaluate the individuals with an invalid fitness
#        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
#        fitnesses = list(map(toolbox.evaluate, invalid_ind))
#        for ind, fit in zip(invalid_ind, fitnesses):
#            ind.fitness.values = fit
#
#        # The population is entirely replaced by the offspring
#        pop[:] = offspring
#        hof.update(pop)
    
    for i in hof:
        print( str(i.fitness.values[0]) + ", " + str(i.fitness.values[1])) 
    
    #return pop, stats, hof
                 
if __name__ == "__main__":
    main()