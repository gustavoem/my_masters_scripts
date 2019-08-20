import sys
sys.path.insert (0, '/home/gustavo/cs/SigNetMS')
from model.SBML import SBML
from experiment.ExperimentSet import ExperimentSet

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


def all_species_modify_measure (V, A, measure):
    """ Decides if for any vertex in V, there is a path that connects 
        this vertex to a vertex that directly affects measure. """
    n = len (V)
    A_inv = [[] for _ in range (n)]
    for v in range (n):
        for v_adj in A[v]:
            A_inv[v_adj].append (v)
    
    reaches = [False] * n
    to_be_visited = []
    for i in range (n):
        if V[i] in measure:
            reaches[i] = True
            to_be_visited.append (i)

    while to_be_visited:
        v = to_be_visited.pop (0)
        for adj in A_inv[v]:
            if not reaches[adj]:
                reaches[adj] = True
                to_be_visited.append (adj)

    for i in range (n):
        if not reaches[i]:
            return False
    return True
        

def disconnects_network (model, reaction_id, experiment_set):
    """ Verifies if, when removing a reaction we disconnect the model.
        By "disconnect" we mean a state in which changing the input
        to the network will not change the output (species present on 
        the measurement expression).
    """
    all_reactions = model.get_all_reactions ()
    measure = experiment_set[0].measure_expression
    for i in range (len (all_reactions)):
        if all_reactions[i].id == reaction_id:
            all_reactions.pop (i)
            break
    vertice, arcs = build_interference_graph (all_reactions)
    return not all_species_modify_measure (vertice, arcs, measure)


def wont_change_measures (model, reaction_json, experiment_set):
    """ Verifies if, when adding a new reaction, the measurements of
        the system won't change. 
    """
    all_reactions = model.get_all_reactions ()
    vertice, arcs = build_interference_graph (all_reactions)
    measure = experiment_set[0].measure_expression
    if not all_species_modify_measure (vertice, arcs, measure):
        raise (ValueError, "The model being evaluated have species" + \
                " that do not have a path of interactions with any" + \
                " of the species present on measurements.")
        return False
    else:
        modified_by_reaction = reaction_json["reactants"] + \
                reaction_json["products"]
        modifies_measure = [s in vertice for s in modified_by_reaction]
        if any (modifies_measure):
            return False
        else:
            return True



parser = argparse.ArgumentParser ()
parser.add_argument ("starting_model", help="An SBML file with the" \
        + " starting node")
parser.add_argument ("interactions_file", help="A JSON file with" \
        + " interactions to be added/removed to the starting model.")
parser.add_argument ("experiments_file", help="An xml file with the" \
        + "experiment performed.")
args = parser.parse_args ()

starting_model_file = args.starting_model
interactions_file = args.interactions_file
experiments_file = args.experiments_file

reactions_json = read_reactions_database (interactions_file)
starting_model = SBML ()
starting_model.load_file (starting_model_file)
starting_subset = define_starting_subset (starting_model, \
        reactions_json)
experiments = ExperimentSet (filename=experiments_file) 

current_model = starting_model.get_copy ()
current_subset = starting_subset.copy ()

print (wont_change_measures (current_model, reactions_json[5], experiments))
print (wont_change_measures (current_model, reactions_json[6], experiments))
print (wont_change_measures (current_model, reactions_json[7], experiments))
print (wont_change_measures (current_model, reactions_json[9], experiments))
#print (disconnects_network (current_model, "SR2", experiments))
#print (disconnects_network (current_model, "SR3", experiments))
