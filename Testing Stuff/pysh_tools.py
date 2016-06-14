# -*- coding: utf-8 -*-
"""
Created on Sun May 22 20:24:23 2016

@author: Eddie
"""
import random

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
    
    """      
    selected_individuals = []    
    
    for i in range(k):
        fit_weights = individuals[0].fitness.weights
        
        candidates = individuals
        cases = list(range(len(individuals[0].fitness.values)))
        random.shuffle(cases)
        
        while len(cases) > 0 and len(candidates) > 1:
            f = min        
            if fit_weights[cases[0]] > 0:
                f = max
            
            best_val_for_case = f(map(lambda x: x.fitness.values[cases[0]], individuals)) 
            
            candidates = list(filter(lambda x: x.fitness.values[cases[0]] == best_val_for_case, individuals))
            cases.pop(0)
                     
        selected_individuals.append(random.choice(candidates))
    
    return selected_individuals