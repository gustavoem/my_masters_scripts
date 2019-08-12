# This scripts takes an sbml file and creates a json file that describes
# all reactions that are present in this file.
#

import sys
import libsbml
import json

model_file = sys.argv[1]
print ("Creating the interactions file for the model", model_file)

# Let's create classes just to organize things...
class Parameter:
    def __init__(self, id_name, value):
        self.id_name = id_name
        self.value = value
        # totally arbitrary
        self.type = "Gamma"
        self.shape = 2
        if value > 2:
            self.scale = 4
        else:
            self.scale = 1


class Reaction:
    def __init__ (self, name, reactants, products, modifiers, \
            parameters, formula):
        self.name = name
        self.reactants = reactants
        self.products = products
        self.modifiers = modifiers
        self.parameters = parameters
        self.formula = formula


def print_reactions_json (reactions):
    json_obj = []
    for reac in reactions:
        reac_json = {}
        reac_json["name"] = reac.name
        reac_json["reactants"] = reac.reactants
        reac_json["products"] = reac.products
        reac_json["modifiers"] = reac.modifiers
        formula = reac.formula
        params_json = []
        for param in reac.parameters:
            param_json = {}
            param_full_name = '_'.join ([param.id_name, reac.name])
            param_json["name"] = param_full_name
            prior_json = {}
            prior_json["type"] = param.type
            prior_json["shape"] = param.shape
            prior_json["scale"] = param.scale
            param_json["prior"] = prior_json
            params_json.append (param_json)
            formula = formula.replace (param.id_name, param_full_name)
        reac_json["parameters"] = params_json
        reac_json["formula"] = formula
        json_obj.append (reac_json)
    f = open ("model_reactions.json", 'w')
    json.dump (json_obj, f, indent=4, ensure_ascii=False)

        


# Load sbml file
reader = libsbml.SBMLReader ()
sbmldoc = reader.readSBML (model_file)
sbmldoc.printErrors ()

# Convert function definitions
converter = libsbml.SBMLFunctionDefinitionConverter ()
converter.setDocument (sbmldoc)
converter.convert ()

# Creates a list of Reaction objects
model = sbmldoc.model
all_reactions = model.getListOfReactions ()
reactions = []
for reaction in all_reactions:
    name_id = reaction.getId ()
    products = [x.species for x in reaction.getListOfProducts ()]
    reactants = [x.species for x in reaction.getListOfReactants ()]
    modifiers = [x.species for x in reaction.getListOfModifiers ()]
    parameters = []
    kinetic_law = reaction.getKineticLaw ()
    formula = kinetic_law.getFormula ()
    reac_params = kinetic_law.getListOfParameters ()
    for p in reac_params:
        id_name = p.getName ()
        value = p.getValue ()
        new_param = Parameter (id_name, value)
        parameters.append (new_param)
    new_reaction = Reaction (name_id, reactants, products, modifiers, \
            parameters, formula)
    reactions.append (new_reaction)
print_reactions_json (reactions)
