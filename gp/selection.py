# _*_ coding: utf_8 _*_
"""
Created on 5/26/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

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
            best_val_for_case = min(list(map(lambda ind: ind.get_errors()[cases[0]], candidates)))
            
            candidates = list(filter(lambda ind: ind.get_errors()[cases[0]] == best_val_for_case, candidates))
            cases.pop(0)
                     
        selected_individuals.append(random.choice(candidates))
    
    return selected_individuals

def tournament_selection(individuals, k, tournament_size):
    '''
    Returns k individuals that do the best out of their respective tournament.
    '''
    selected_individuals = []
    for i in range(k):
        tournament = []
        for i in range(tournament_size):
            tournament.append(random.choice(individuals))
        min_error_in_tourn = min(list(map(lambda ind: ind.get_total_error(), tournament)))
        best_in_tourn = list(filter(lambda ind: ind.get_total_error() == min_error_in_tourn, tournament))
        selected_individuals.append(best_in_tourn[0])
    return selected_individuals