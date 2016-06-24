# -*- coding: utf-8 -*-
"""
Created on Sun May 22 20:24:23 2016

@author: Eddie
"""
import random
import numpy

from scoop import futures

#####################
# Utility Functions #
#####################

def protected_division(numerator, denominator):
    if denominator is 0:
        return 1
    else:
        return numerator / denominator

def group_by (func, l):
    """
    Returns a map of the elements of l keyed by the result of
    func on each element. The value at each key will be a list of the
    corresponding elements, in the order they appeared in l.
    Same as Clojure's group_by.
    """
    result = {}
    for e in l:
        x = func(e)
        if (x in result):
            result[x].append(e)
        else:
            result[x] = [e]
    return result
    


##################
# Pysh Operators #
##################

def lexicase_selection(individuals, k):
    """
    Returns an individual that does the best on the fitness cases when considered one at a
    time in random order.
    http://faculty.hampshire.edu/lspector/pubs/lexicase-IEEE-TEC.pdf
    """      
    selected_individuals = []    
    
    for i in range(k):
        fit_weights = individuals[0].fitness.weights
        
        candidates = individuals
        cases = list(range(len(individuals[0].fitness.values)))
        random.shuffle(cases)
        
        while len(cases) > 0 and len(candidates) > 1:
            #print(':')
            f = min        
            if fit_weights[cases[0]] > 0:
                f = max
            
            best_val_for_case = f(futures.map(lambda x: x.fitness.values[cases[0]], individuals)) 
            
            candidates = list(filter(lambda x: x.fitness.values[cases[0]] == best_val_for_case, individuals))
            cases.pop(0)
                     
        selected_individuals.append(random.choice(candidates))
    
    return selected_individuals


def epsilon_lexicase_selection(individuals, k, epsilon):
    """
    Returns an individual that does the best on the fitness cases when considered one at a
    time in random order. Requires a epsilon parameter.
    https://push-language.hampshire.edu/uploads/default/original/1X/35c30e47ef6323a0a949402914453f277fb1b5b0.pdf
    Implemented epsilon_y implementation.
    """      
    selected_individuals = []    
    
    for i in range(k):
        fit_weights = individuals[0].fitness.weights
        
        candidates = individuals
        cases = list(range(len(individuals[0].fitness.values)))
        random.shuffle(cases)
        
        while len(cases) > 0 and len(candidates) > 1:
            #print(':')      
            if fit_weights[cases[0]] > 0:
                best_val_for_case = max(map(lambda x: x.fitness.values[cases[0]], individuals)) 
                min_val_to_survive_case = best_val_for_case - epsilon
                candidates = list(filter(lambda x: x.fitness.values[cases[0]] >= min_val_to_survive_case, individuals))
            else :
                best_val_for_case = min(map(lambda x: x.fitness.values[cases[0]], individuals)) 
                max_val_to_survive_case = best_val_for_case + epsilon
                candidates = list(filter(lambda x: x.fitness.values[cases[0]] <= max_val_to_survive_case, individuals))
            
            cases.pop(0)
                     
        selected_individuals.append(random.choice(candidates))
    
    return selected_individuals

def adaptive_epsilon_lexicase_selection(individuals, k):
    """
    Returns an individual that does the best on the fitness cases when considered one at a
    time in random order. 
    https://push-language.hampshire.edu/uploads/default/original/1X/35c30e47ef6323a0a949402914453f277fb1b5b0.pdf
    Implemented lambda_epsilon_y implementation.
    """      
    selected_individuals = []    
    
    for i in range(k):
        fit_weights = individuals[0].fitness.weights
        
        candidates = individuals
        cases = list(range(len(individuals[0].fitness.values)))
        random.shuffle(cases)
        
        while len(cases) > 0 and len(candidates) > 1:
            median_val = numpy.median(map(lambda x: x.fitness.values[cases[0]], individuals))
            median_absolute_deviation = numpy.median(map(lambda x: [abs(j - median_val) for j in x.fitness.values[cases[0]]], individuals))   
            if fit_weights[cases[0]] > 0:
                best_val_for_case = max(map(lambda x: x.fitness.values[cases[0]], individuals)) 
                min_val_to_survive = best_val_for_case - median_absolute_deviation
                candidates = list(filter(lambda x: x.fitness.values[cases[0]] >= min_val_to_survive, individuals))
            else :
                best_val_for_case = min(map(lambda x: x.fitness.values[cases[0]], individuals)) 
                max_val_to_survive = best_val_for_case + median_absolute_deviation
                candidates = list(filter(lambda x: x.fitness.values[cases[0]] <= min_val_to_survive, individuals))
            
            cases.pop(0)
                     
        selected_individuals.append(random.choice(candidates))
    
    return selected_individuals

