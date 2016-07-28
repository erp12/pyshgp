# _*_ coding: utf_8 _*_
"""
Created on 5/26/2016

@author: Eddie
"""
import random


#####################
# Selection Methods #
#####################

def lexicase_selection(individuals, k):
    """
    Returns an individual that does the best on the fitness cases when considered one at a
    time in random order.
    http://faculty.hampshire.edu/lspector/pubs/lexicase-IEEE-TEC.pdf
    """
    selected_individuals = []    
    
    for i in range(k):        
        candidates = individuals
        cases = list(range(len(individuals[0].get_errors())))
        random.shuffle(cases)
        
        while len(cases) > 0 and len(candidates) > 1:
            best_val_for_case = min(map(lambda ind: ind.get_errors()[cases[0]], individuals))
            
            candidates = list(filter(lambda ind: ind.get_errors()[cases[0]] == best_val_for_case, individuals))
            cases.pop(0)
                     
        selected_individuals.append(random.choice(candidates))
    
    return selected_individuals

def tournament_selection(individuals, k):
	'''
	Returns k individuals that do the best out of their respective tournament.
	'''
	raise Exception("tournament_selection not implemented yet!")

