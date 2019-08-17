import json
import argparse

def read_reactions_database (db_file):
    """ Reads the json file with all reactions. """
    raw_reactions = json.load (db_file)
    return raw_reactions


def create_reaction_object (reaction_json):
    """ Create a Reaction object given a json reaction. """
    id_name = reaction_json["name"]
    reactants = reaction_json["reactants"]
    products = reaction_json["products"]
    modifiers = reaction_json["modifiers"]
    parameters = reaction_json["parameters"]
    [p["value"] = 0 for p in parameters]
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

starting_model = args.starting_model
interactions_file = args.interactions_file
reactions_json = read_reactions_database (interactions_file)

starting_subset = define_starting_subset (current_model)
