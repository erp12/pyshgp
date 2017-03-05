# _*_ coding: utf_8 _*_
"""
Created on 9/19/2016

@author: Eddie
"""
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import random
import numpy  as np
import pandas as pd

import pysh.utils as u
import pysh.gp.gp as gp
import pysh.push.interpreter as interp
import pysh.push.instructions.registered_instructions as ri
import pysh.push.instruction as instr

# Get the absolute path to the data file
script_dir = os.path.dirname(__file__)
rel_path = "../data/credit.csv"
abs_file_path = os.path.join(script_dir, rel_path)

# Load the data file and split into training and testing.
credit_data = pd.read_csv(abs_file_path)
train_inds = np.random.rand(len(credit_data)) < 0.8
training_set = credit_data[train_inds]
testing_set = credit_data[~train_inds]

def random_one_character_str():
    return random.choice("abcdefghijklmnopqrstuvwxyz0123456789")

def random_two_character_str():
    s = random.choice("abcdefghijklmnopqrstuvwxyz0123456789")
    return s + random.choice("abcdefghijklmnopqrstuvwxyz0123456789")

def credit_error_func(program, debug = False):
    errors = []

    for index, row in training_set.iterrows():
        # Create the push interpreter
        interpreter = interp.PushInterpreter()
        interpreter.reset_pysh_state()
        
        # Push input number     
        interpreter.state.stacks["_input"].push_item(row['V1'])
        interpreter.state.stacks["_input"].push_item(row['V2'])
        interpreter.state.stacks["_input"].push_item(row['V3'])
        interpreter.state.stacks["_input"].push_item(row['V4'])
        interpreter.state.stacks["_input"].push_item(row['V5'])
        interpreter.state.stacks["_input"].push_item(row['V6'])
        interpreter.state.stacks["_input"].push_item(row['V7'])
        interpreter.state.stacks["_input"].push_item(row['V8'])
        interpreter.state.stacks["_input"].push_item(row['V9'])
        interpreter.state.stacks["_input"].push_item(row['V10'])
        interpreter.state.stacks["_input"].push_item(row['V11'])
        interpreter.state.stacks["_input"].push_item(row['V12'])
        interpreter.state.stacks["_input"].push_item(row['V13'])
        interpreter.state.stacks["_input"].push_item(row['V14'])
        interpreter.state.stacks["_input"].push_item(row['V15'])

        # Initialize output classes
        interpreter.state.stacks["_output"].push_item(0)
        interpreter.state.stacks["_output"].push_item(0)

        # Run program
        interpreter.run_push(program, debug)

        # Get output
        class_votes = interpreter.state.stacks['_output'][1:]

        if int(row['V16']) == class_votes.index(max(class_votes)):
            errors.append(0)
        else:
            errors.append(1)

    return errors

credit_params = {
    "error_threshold" : 20, # If under 20 rows are mis-classified, consider the program a solution.
    "population_size" : 1000,
    "max_genome_initial_size" : 100,
    "max_points" : 400,
    "atom_generators" : list(u.merge_sets(ri.registered_instructions,
                                          [lambda: random.randint(0, 100),
                                           lambda: random.random(),
                                           lambda: random_one_character_str(),
                                           lambda: random_one_character_str(),
                                           # Inpput instructions
                                           instr.PyshInputInstruction(0),
                                           instr.PyshInputInstruction(1),
                                           instr.PyshInputInstruction(2),
                                           instr.PyshInputInstruction(3),
                                           instr.PyshInputInstruction(4),
                                           instr.PyshInputInstruction(5),
                                           instr.PyshInputInstruction(6),
                                           instr.PyshInputInstruction(7),
                                           instr.PyshInputInstruction(8),
                                           instr.PyshInputInstruction(9),
                                           instr.PyshInputInstruction(10),
                                           instr.PyshInputInstruction(11),
                                           instr.PyshInputInstruction(12),
                                           instr.PyshInputInstruction(13),
                                           instr.PyshInputInstruction(14),
                                           # Class label voting instsructions.
                                           instr.PyshClassVoteInstruction(1, '_float'),
                                           instr.PyshClassVoteInstruction(1, '_integer'),
                                           instr.PyshClassVoteInstruction(2, '_float'),
                                           instr.PyshClassVoteInstruction(2, '_integer')
                                          ])),
    "genetic_operator_probabilities" : {"alternation" : 0.3,
                                        "uniform_mutation" : 0.3,
                                        "alternation & uniform_mutation" : 0.3,
                                        "uniform_close_mutation" : 0.1},
    "selection_method" : "lexicase",
    "uniform_mutation_constant_tweak_rate" : 0.1,
    "uniform_mutation_float_gaussian_standard_deviation" : 0.1
}

def test_credit_solution():
    #print(registered_instructions.registered_instructions)
    prog_lst = [1.5, instr.PyshClassVoteInstruction(1, '_float')]
    prog = gp.load_program_from_list(prog_lst)
    errors = credit_error_func(prog, debug = True)
    print("Errors:", errors)
    print("Total Errors:", sum(errors))

if __name__ == "__main__":
    gp.evolution(credit_error_func, credit_params)
    #test_credit_solution()


