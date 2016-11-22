# _*_ coding: utf_8 _*_
"""
Created on 5/26/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import random
import numpy as np

#####################
# Selection Methods #
#####################

def lexicase_selection(individuals, k = 1):
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
            best_val_for_case = min([ind.get_errors()[cases[0]] for ind in candidates])
            
            candidates = [ind for ind in candidates if ind.get_errors()[cases[0]] == best_val_for_case]
            cases.pop(0)
                     
        selected_individuals.append(random.choice(candidates))
    
    return selected_individuals

def epsilon_lexicase_selection(individuals, epsilon = None, k = 1):
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
            errors_for_this_case = [ind.get_errors()[cases[0]] for ind in candidates]
            best_val_for_case = min(errors_for_this_case)

            if epsilon == None:
                median_val = np.median(errors_for_this_case)
                median_absolute_deviation = np.median([abs(x - median_val) for x in errors_for_this_case])
                epsilon = median_absolute_deviation
            candidates = [ind for ind in candidates if ind.get_errors()[cases[0]] <= best_val_for_case + epsilon]
            cases.pop(0)

        selected_individuals.append(random.choice(candidates))

    return selected_individuals

def cluster_lexicase_selection(population, clusters, k = 1):
    centers = clusters.cluster_centers_

    selected_clusters = []

    #non_empty_clusers = list(filter(lambda x: x in clusters.labels_, list(range(len(clusters.cluster_centers_)))))
    non_empty_clusers = [x for x in list(range(len(clusters.cluster_centers_))) if x in clusters.labels_]

    for i in range(k):
        candidates = non_empty_clusers
        cases = list(range(len(centers[0])))
        random.shuffle(cases)

        while len(cases) > 0 and len(candidates) > 1:
            best_val_for_cases = min([centers[cluster][cases[0]] for cluster in candidates])

            candidates = [cluster for cluster in candidates if centers[cluster][cases[0]] == best_val_for_cases] 
            cases.pop(0)

        selected_clusters.append(random.choice(candidates))
    
    selected_individuals = []
    for cl in selected_clusters:
        inds_in_cluster = [population[i] for i in list(range(len(population))) if clusters.labels_[i] == cl]
        selected_individuals.append(random.choice(inds_in_cluster))

        
    return selected_individuals

def tournament_selection(individuals, tournament_size, k = 1):
    '''
    Returns k individuals that do the best out of their respective tournament.
    '''
    selected_individuals = []
    for i in range(k):
        tournament = []
        for _ in range(tournament_size):
            tournament.append(random.choice(individuals))
        min_error_in_tourn = min([ind.get_total_error() for ind in tournament])
        best_in_tourn = [ind for ind in tournament if ind.get_total_error() == min_error_in_tourn]
        selected_individuals.append(best_in_tourn[0])
    return selected_individuals


#############################
# Master Selection Function #
#############################

def selection(population, evolutionary_params, k = 1,):
    if evolutionary_params["selection_method"] == "lexicase":
        return lexicase_selection(population, k)
    elif evolutionary_params["selection_method"] == "epsilon_lexicase":
        return epsilon_lexicase_selection(population, evolutionary_params["epsilon_lexicase_epsilon"], k)
    elif evolutionary_params["selection_method"] == "tournament":
        return tournament_selection(population, evolutionary_params["tournament_size"], k)
    elif evolutionary_params["selection_method"] == "cluster_lexicase":
        return cluster_lexicase_selection(population, evolutionary_params["clusters"], k)
    else:
        raise Exception("Unknown selection method: " + str(evolutionary_params["selection_method"]))