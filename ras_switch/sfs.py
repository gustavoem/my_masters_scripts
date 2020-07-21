from pathlib import Path
# SIGNET_MS_PATH =  '/project/msreis/modelSelection/project/SigNetMS'
SIGNET_MS_PATH = '/home/gestrela/SigNetMS'
#SIGNET_MS_PATH = '/home/gustavo/cs/SigNetMS'
CURRENT_PATH = str (Path ().absolute ())

import sys
sys.path.insert (0, SIGNET_MS_PATH)
from model.SBML import SBML
from model.RandomParameter import RandomParameter
from model.RandomParameterList import RandomParameterList
from model.PriorsWriter import write_priors_file
from model.Reaction import Reaction
from experiment.ExperimentSet import ExperimentSet
from distributions.Gamma import Gamma
from SigNetMS import perform_marginal_likelihood
import numpy as np
import os
import json
import argparse
import random
import time


def model_has_reaction (model, reac):
    """ Returns true if model contains the reaction. """
    all_model_rections = model.get_all_reactions ()
    for model_reac in all_model_rections:
        if model_reac.id == reac["name"]:
            return True
    return False


def define_starting_subset (model, reactions):
    """ Determine the reactions that are present in model. """
    is_present_array = [0] * len (reactions)
    for i in range (len (reactions)):
        is_present_array[i] = model_has_reaction (model, reactions[i])
    return is_present_array


def read_reactions_database (db_file):
    """ Reads the json file with all reactions. """
    db_file_obj = open (db_file)
    raw_reactions = json.load (db_file_obj)
    return raw_reactions


def create_reaction_object (reaction_json):
    """ Create a Reaction object given a json reaction. """
    id_name = reaction_json["name"]
    reactants = reaction_json["reactants"]
    products = reaction_json["products"]
    modifiers = reaction_json.get("modifiers") or []
    parameters = reaction_json["parameters"]
    for p in parameters:
        p["value"] = 0
    formula = reaction_json["formula"]
    reaction = Reaction (id_name, reactants, products, modifiers, \
            parameters, formula)
    return reactions


def build_interference_graph (reaction_list):
    """ Build a graph that says which species interact directly changes
        the concentration of other species over time. """
    V = []
    A = []
    for reaction in reaction_list:
        for species in (reaction.reactants + reaction.modifiers):
            if species not in V:
                species_idx = len (V)
                V.insert (species_idx, species)
                A.insert (species_idx, [])
            species_idx = V.index (species)
            for adjacent_species in reaction.products:
                if adjacent_species not in V:
                    adjacent_species_idx = len (V)
                    V.insert (adjacent_species_idx, adjacent_species)
                    A.insert (adjacent_species_idx, [])
                adjacent_species_idx = V.index (adjacent_species)
                A[species_idx].append (adjacent_species_idx)
    return V, A
        

def get_vertice_that_reach (V, A, target_set):
    """ Returns a list of all vertice in V that will reach vertice from
        the set target_set. """
    inv_A = [[] for v in V]
    nV = len (V)
    for v in range (nV):
        for adj in A[v]:
            inv_A[adj].append (v)

    reaches = []
    search_queue = []
    visited = [False for v in V]
    for v in range (nV):
        if V[v] in target_set:
            search_queue.append (v)
            visited[v] = True
            reaches.append (V[v])

    while search_queue:
        current_node = search_queue.pop (0)
        for adj in inv_A[current_node]:
            if visited[adj]:
                continue
            reaches.append (V[adj])
            visited[adj] = True
            search_queue.append (adj)
    return reaches


def changes_measures (model, reaction_json, experiment_set):
    """ Verifies if, when adding a new reaction, the measurements of
        the system won't change. 
    """
    all_reactions = model.get_all_reactions ()
    vertice, arcs = build_interference_graph (all_reactions)
    measure = experiment_set[0].measure_expression
    measure_species = [v for v in vertice if v in measure]
    reaching_v = get_vertice_that_reach (vertice, arcs, measure_species)
    print ("Verifying the reaction: ", end='')
    print (' + '.join (reaction_json["reactants"]), end='')
    print ('---', end='')
    print (''.join (reaction_json.get("modifiers") or []), end='')
    print ('-->', end='')
    print (' + '.join (reaction_json["products"]))
    for s in (reaction_json["reactants"] + reaction_json["products"]):
        if s in reaching_v:
            return True
    return False


def create_subset_dir (subset):
    """ Creates the subset that will store the input files of a model. 
    """
    subset_str = 'subset_' + ''.join ([str (int (x)) for x in subset])
    os.mkdir (subset_str)
    return subset_str


def define_priors (subset, reaction_json, subset_directory):
    """ Creates a prior file for a subset of reactions and places it
        inside the subset directory. """
    n = len (reaction_json)
    subset_reacts = [reaction_json[i] for i in range (n) if subset[i]]
    theta = RandomParameterList ()
    for reac in subset_reacts:
        params = reac["parameters"]
        for param in params:
            name = param["name"]
            distribution = Gamma (param["prior"]["shape"], \
                    param["prior"]["scale"])
            p = RandomParameter (name, distribution)
            theta.append (p)
    sigma_dist = Gamma (2, .1)
    sigma = RandomParameter ('Noise', sigma_dist)
    theta.set_experimental_error (sigma) 
    write_priors_file (subset_directory + '/model.priors', theta)


def save_model_file (model, subset_directory):
    model.set_name (subset_directory.replace ("subset", "model"))
    model.write_sbmldoc_to_file (subset_directory + '/model.sbml')


def add_reaction_to_model (model, reaction_json):
    """ Adds a reaction (in json format) to an SBML model."""
    id_name = reaction_json["name"]
    reactants = reaction_json["reactants"]
    products = reaction_json["products"]
    modifiers = reaction_json.get("modifiers") or []
    parameters = []
    for p_json in reaction_json["parameters"]:
        p = {}
        p["name"] = p_json["name"]
        p["value"] = 1
        parameters.append (p)
    formula = reaction_json["formula"]
    reaction = Reaction (id_name, reactants, products, modifiers, \
            parameters, formula)
    model.add_reaction (reaction)


def calculate_score (subset_directory, exp_file, seed):
    """ Given the subset of a model, calculates the score of this model.
    """
    subset_dir_path = CURRENT_PATH + '/' + subset_directory
    model_file = subset_dir_path + '/model.sbml'
    priors_file = subset_dir_path + '/model.priors'
    sample_file = subset_dir_path + '/sample.txt'
    exp_file = CURRENT_PATH + '/' + exp_file
    start = time.time()
    try:
        score = 0
        score = (-1) * perform_marginal_likelihood (
                model_file,
                priors_file,
                exp_file,
                15000,
                1000,
                3000,
                3000,
                n_process=15,
                sample_output_file=sample_file,
                seed=seed
        )
    except ValueError:
        print ("There was no convergence of parameters in burn-in" \
                + " sampling.")
        score = None
    except Exception as e:
        print ("Something else happened")
        print (e)
        score = None
    end = time.time()
    return score, end - start


def get_candidate_reactions (current_subset):
    return [i for i in range (len (current_subset)) if not 
            current_subset[i]]

def prepare_input (subset, model, reactions_json):
    subset_dir = create_subset_dir (subset)
    define_priors (subset, reactions_json, subset_dir)
    save_model_file (model, subset_dir)
    return subset_dir



parser = argparse.ArgumentParser ()
parser.add_argument ("starting_model", help="An SBML file with the" \
        + " starting node")
parser.add_argument ("interactions_file", help="A JSON file with" \
        + " interactions to be added/removed to the starting model.")
parser.add_argument ("experiments_file", help="An xml file with the" \
        + "experiment performed.")
parser.add_argument ("--seed", type=int, nargs='?', default=0, help="Seed for random number" \
        + "generator.")
args = parser.parse_args ()

starting_model_file = args.starting_model
interactions_file = args.interactions_file
experiments_file = args.experiments_file
seed =  args.seed

# random seed to chain generation
random.seed(seed)

reactions_json = read_reactions_database (interactions_file)
starting_model = SBML ()
starting_model.load_file (starting_model_file)
starting_subset = define_starting_subset (starting_model, \
        reactions_json)
experiments = ExperimentSet (filename=experiments_file) 

current_model = starting_model.get_copy ()
current_subset = starting_subset.copy ()

computed_subsets = {}
scores_filename = 'subsets_scores.txt'

current_subset_dir = prepare_input (current_subset, current_model, 
        reactions_json)
score, elapsed_time = calculate_score (current_subset_dir,
        experiments_file, seed)

current_subset_str = ''.join (str (int (b)) for b in current_subset)
computed_subsets[current_subset_str] = score
scores_file = open (scores_filename, 'a')
scores_file.write (current_subset_str + ': ' + str (score))
scores_file.write (', ' + str (elapsed_time) + '\n')
scores_file.close ()


# Sequential Forward Search
n = len (reactions_json)
while sum (current_subset) < n:
    print ("\n-------------\nNew iteration")
    print ("Current subset: ", current_subset_str)
    scores_file = open (scores_filename, 'a')
    scores_file.write ("Current subset: " + current_subset_str + "\n")
    scores_file.close ()

    
    candidates = get_candidate_reactions (current_subset)
    print ("Candidate reactions to be added (indexes): ", candidates) 
    
    best_candidate_str = None
    best_candidate = None

    for candidate in candidates:
        candidate_reaction = reactions_json[candidate]
        candidate_subset = current_subset.copy()
        candidate_subset[candidate] = True
        candidate_subset_str = ''.join (str (int (b)) for b in
                candidate_subset)
        candidate_model = current_model.get_copy ()
        add_reaction_to_model (candidate_model, candidate_reaction)
        candidate_dir = prepare_input (candidate_subset,
                candidate_model, reactions_json)

        score = 0
        elapsed_time = 0
        if not changes_measures (current_model, candidate_reaction,
                experiments):
            score = computed_subsets[current_subset_str]
        else:
            score, elapsed_time = calculate_score (candidate_dir,
                experiments_file, seed)

        computed_subsets[candidate_subset_str] = score
        if best_candidate is None or \
        computed_subsets[best_candidate_str] > score:
            best_candidate_str = candidate_subset_str
            best_candidate = candidate
        
        scores_file = open (scores_filename, 'a')
        scores_file.write (candidate_subset_str + ': ' + str (score))
        scores_file.write (', ' + str (elapsed_time) + '\n')
        scores_file.close ()

        print("\t" + current_subset_str + ": " + str (score))
    
    current_subset[best_candidate] = True
    current_subset_str = ''.join (str (int (b)) for b in current_subset)
    best_reaction = reactions_json[best_candidate]
    add_reaction_to_model (current_model, best_reaction)

print ("Current subset: ", current_subset_str)
scores_file = open (scores_filename, 'a')
scores_file.write ("Current subset: " + current_subset_str + "\n")
scores_file.close ()

