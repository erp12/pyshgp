# _*_ coding: utf_8 _*_
"""
Created on 5/50/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import math
import random

from .. import exceptions as e

from ..push import plush as pl
from ..push import random as r

from . import selection as sel
from . import individual


#############
# Utilities #
#############

def gaussian_noise_factor():
    '''Returns gaussian noise of mean 0, std dev 1.
    '''
    return math.sqrt(-2.0 * math.log(random.random())) * math.cos(2.0 * math.pi * random.random()) 

def perturb_with_gaussian_noise(sd, n):
    '''Returns n perturbed with std dev sd.
    '''
    return n + (sd * gaussian_noise_factor())


#############################
# Crossover and Alternation #
#############################

def alternation(parent_1, parent_2, evo_params):
    """Uniformly alternates between the two parents. parent_1 and parent_2 are plush genomes.
    """
    resulting_genome = []

    # Random pick which parent to start from
    use_parent_1 = random.choice([True, False])

    loop_times = len(parent_1)
    if not use_parent_1:
        loop_times = len(parent_2)

    i = 0
    while (i < loop_times) and (len(resulting_genome) < evo_params["max_points"]):
        if random.random() < evo_params["alternation_rate"]:
            # Switch which parent we are pulling genes from
            i += round(evo_params["alignment_deviation"] * gaussian_noise_factor())
            i = int(max(0, i))
            use_parent_1 = not use_parent_1
        else:
            # Pull gene from parent
            if use_parent_1:
                resulting_genome.append(parent_1[i])
            else:
                resulting_genome.append(parent_2[i])
            i = int(i+1)

        # Change loop stop condition
        loop_times = len(parent_1)
        if not use_parent_1:
            loop_times = len(parent_2)

    return resulting_genome


#############
# Mutations #
#############

# Uniform Mutation

def string_tweak(s, evo_params):
    new_s = ""
    for c in s:
        if random.random() < evo_params['uniform_mutation_string_char_change_rate']:
            new_s += random.choice(['\t', '\n'] + list(map(chr, range(32, 127))))
        else:
            new_s += c
    return new_s

def instruction_mutator(evo_params):
    return r.random_plush_instruction(evo_params)

def constant_mutator(token, evo_params):
    if pl.plush_gene_is_literal(token):
        const = pl.plush_gene_get_instruction(token)
        instruction = None

        if type(const) == float:
            instruction = perturb_with_gaussian_noise(evo_params["uniform_mutation_float_gaussian_standard_deviation"], const)
        elif type(const) == int:
            instruction = round(perturb_with_gaussian_noise(evo_params["uniform_mutation_float_gaussian_standard_deviation"], const))
        elif type(const) == str:
            instruction = string_tweak(const, evo_params)
        elif type(const) == bool:
            instruction = random.choice([True, False])
        return pl.make_plush_gene(instruction, True, token[2], token[3])
    else:
        return instruction_mutator(evo_params)

def token_mutator(token, evo_params):
    new_token = token
    if random.random() < evo_params["uniform_mutation_rate"]:
        if random.random() < evo_params["uniform_mutation_constant_tweak_rate"]:
            new_token = constant_mutator(token, evo_params)
        else:
            new_token = instruction_mutator(evo_params)
    return new_token

def uniform_mutation(genome, evo_params):
    """
    Uniformly mutates individual. For each token in program, there is
    uniform-mutation-rate probability of being mutated. If a token is to be
    mutated, it has a uniform-mutation-constant-tweak-rate probability of being
    mutated using a constant mutator (which varies depending on the type of the
    token), and otherwise is replaced with a random instruction.
    """
    new_genome = [token_mutator(gene, evo_params) for gene in genome]
    return new_genome

# Uniform Close Mutation

def close_mutator(gene, evo_params):
    closes = pl.plush_gene_get_closes(gene)

    new_closes = None
    if random.random() < evo_params['uniform_close_mutation_rate']:
        if random.random() < evo_params['close_increment_rate']:
            new_closes = closes + 1
        else:
            if closes == 0:
                new_closes = 0
            else:
                new_closes =  closes - 1
    else:
        new_closes = closes

    return pl.make_plush_gene(pl.plush_gene_get_instruction(gene),
                              pl.plush_gene_is_literal(gene),
                              new_closes,
                              pl.plush_gene_is_silent(gene))

def uniform_close_mutation(genome, evo_params):
    """
    Uniformly mutates the _close's in the individual's instruction maps. Each
    _close will have a uniform_close_mutation_rate probability of being changed,
    and those that are changed have a close_increment_rate chance of being
    incremented, and are otherwise decremented.
    """
    if not "_close" in evo_params["epigenetic_markers"]:
        return genome
    return [close_mutator(gene, evo_params) for gene in genome]


#############################
# Master Genetics Functions #
#############################

def produce_child(population, genetic_operators, evolutionary_params):
    '''
    Returns one offspring individual.
    '''
    child = sel.selection(population, evolutionary_params)[0]
    ops = genetic_operators.split(" & ")
    for op in ops:
        op = str(op)
        if op == "alternation":
            # Apply alternation
            other_parent = sel.selection(population, evolutionary_params)[0]
            child_genome = alternation(child.get_genome(), 
                                       other_parent.get_genome(), 
                                       evolutionary_params)
            child = individual.Individual(child_genome, evolutionary_params)
        elif op == "uniform_mutation":
            # Apply uniform mutation
            child_genome = uniform_mutation(child.get_genome(), evolutionary_params)
            child = individual.Individual(child_genome, evolutionary_params)
        elif op == "uniform_close_mutation":
             # Apply uniform close mutation
            child_genome = uniform_close_mutation(child.get_genome(), evolutionary_params)
            child = individual.Individual(child_genome, evolutionary_params)
        else:
            raise e.UnknownGeneticOperator(op)
    return child

def produce_n_children(n, population, genetic_operators, evolutionary_params):
    return [produce_child(population, genetic_operators, evolutionary_params) for x in range(n)]

def genetics(population, evolutionary_params):
    '''
    Returns the next generation (unevaluated)
    '''

    # Create next generation
    offspring = []
    # Calculate number of children that should be made from each genetic operator
    num_offspring_each_gen_op = dict([(k, int(round(evolutionary_params["genetic_operator_probabilities"][k] * evolutionary_params["population_size"]))) for k in evolutionary_params["genetic_operator_probabilities"]])
    
    if evolutionary_params['parallel_genetics'] and (evolutionary_params["max_workers"] == None or evolutionary_params["max_workers"] > 1):
        
        # Have to figure out how to divide the population in to n groups while preserving gen op numbers.
        jobs_n = []
        jobs_ops = []

        pool = evolutionary_params['pool']
        aprox_num_individuals_per_job = int(evolutionary_params["population_size"] / (pool.ncpus - 1))

        for op in num_offspring_each_gen_op.keys():
            i = num_offspring_each_gen_op[op]
            while i > 0:
                if i < aprox_num_individuals_per_job:
                    jobs_n.append(i)
                    jobs_ops.append(op)
                    i -= i
                else:
                    jobs_n.append(aprox_num_individuals_per_job)
                    jobs_ops.append(op)
                    i -= aprox_num_individuals_per_job

        job_results = pool.map(produce_n_children, 
                               jobs_n,
                               [population]*len(jobs_n),
                               jobs_ops,
                               [evolutionary_params]*len(jobs_n))

        for jr in job_results:
            offspring += jr

    else :
        # For each operator or operator combination
        for op in num_offspring_each_gen_op.keys():
            # For each child that should be made by `op`
            for i in range(num_offspring_each_gen_op[op]):
                offspring.append(produce_child(population, op, evolutionary_params))

    return offspring

