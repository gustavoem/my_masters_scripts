import sys
sys.path.insert (0, '/home/gustavo/cs/SigNetMS')
from model.SBML import SBML

import json
import argparse


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
        is_present_array[i] = \
                int (model_has_reaction (model, reactions[i]))
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


parser = argparse.ArgumentParser ()
parser.add_argument ("starting_model", help="An SBML file with the" \
        + " starting node")
parser.add_argument ("interactions_file", help="A JSON file with" \
        + " interactions to be added/removed to the starting model.")
args = parser.parse_args ()

starting_model_file = args.starting_model
interactions_file = args.interactions_file

reactions_json = read_reactions_database (interactions_file)
starting_model = SBML ()
starting_model.load_file (starting_model_file)
starting_subset = define_starting_subset (starting_model, \
        reactions_json)
print (starting_subset)


current_model = starting_model.get_copy ()
current_subset = starting_subset.copy ()
