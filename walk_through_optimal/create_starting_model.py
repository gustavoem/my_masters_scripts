from pathlib import Path
SIGNET_MS_PATH =  '/home/gustavo/cs/SigNetMS'
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
import os
import json
import argparse
import random


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
    modifiers = reaction_json["modifiers"]
    parameters = reaction_json["parameters"]
    for p in parameters:
        p["value"] = 0
    formula = reaction_json["formula"]
    reaction = Reaction (id_name, reactants, products, modifiers, \
            parameters, formula)
    return reactions



def save_model_file (model, subset_directory):
    model.set_name (subset_directory.replace ("subset", "model"))
    model.write_sbmldoc_to_file (subset_directory + '/model.sbml')


def add_reaction_to_model (model, reaction_json):
    """ Adds a reaction (in json format) to an SBML model."""
    id_name = reaction_json["name"]
    reactants = reaction_json["reactants"]
    products = reaction_json["products"]
    modifiers = reaction_json["modifiers"]
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


def remove_reaction (model, reaction_id):
    model.remove_reaction (reaction_id)


model = SBML ()
model.load_file ('base_model.sbml')
remove_reaction (model, 'SR2')
remove_reaction (model, 'SR3')
remove_reaction (model, 'SR4')
remove_reaction (model, 'SR5')

reactions_json = read_reactions_database ('all_interaction.json')

reactions_to_add = ["R5", "R6", "R9", "R10"]
react_to_add_idxs = [i for i in range (len (reactions_json)) \
        if reactions_json[i]["name"] in reactions_to_add]
for idx in react_to_add_idxs:
    add_reaction_to_model (model, reactions_json[idx])
model.write_sbmldoc_to_file ('starting_model.sbml')
