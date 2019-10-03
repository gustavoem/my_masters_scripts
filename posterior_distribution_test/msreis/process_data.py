from pathlib import Path
SIGNET_MS_PATH =  '/home/gustavo/cs/SigNetMS'
CURRENT_PATH = str (Path ().absolute ())

import os
import sys
sys.path.insert (0, SIGNET_MS_PATH)
import re
from model.SBML import SBML
from model.PriorsReader import define_sbml_params_priors


# Find the model directories
subdirs = [subdir[0] for subdir in os.walk (CURRENT_PATH)]
all_dirs = [subdir for subdir in subdirs if 'subset' in subdir]
model_dirs = []

subset_regex = re.compile (".*msreis\/(subset_\d+)")
# Find the parameter order for each model
model_params = {}
for current_dir in all_dirs:
    model_dir_match = subset_regex.match (current_dir)
    print (model_dir_match)
    if not model_dir_match:
        continue
    
    model_dirs.append (current_dir)
    subset = model_dir_match.group (1)
    priors_file = current_dir + '/model.priors'
    model_file = current_dir + '/model.sbml'
    model_sbml = SBML ()
    model_sbml.load_file (model_file)
    theta_priors = define_sbml_params_priors (model_sbml, 
            priors_file)
    param_names = [] 
    # ignore observation noise parameter, which is the last
    for p in theta_priors[:-1]:
        original_name = model_sbml.get_original_param_name (p.name)
        param_names.append (original_name)
    model_params[subset] = param_names
models = list (model_params.keys ())


output_file = 'surface_walk_results.txt'
out = open (output_file, 'w')

current_dir = os.getcwd ()
pop_temp_regex = re.compile ("Sample for t = " + \
        "(\d*\.\d+(?:e(?:\-|\+)\d+)?)")
parameter_regex = re.compile ("parameter = \[(.*)\]")


# First lines of the output is the header:
# model1_name parameters_of_the_model1
# model2_name parameters_of_the_model2
# ...
# modelm_name parameters_of_the_modelm
for m in models:
    line = m + ' ' + ' '.join (model_params[m]) + '\n'
    out.write (line)

for model_dir in model_dirs:
    output_file_name = model_dir + '/sample.txt'
    output_file = open (output_file_name)
    current_temperature = 0 
    current_subset = subset_regex.match (model_dir).group (1)
    print (current_subset)
    for line in output_file:
        m = pop_temp_regex.match (line)
        if m:
            current_temperature = float (m.group (1))
        m = subset_regex.match (line)
        if m:
            current_subset = models.index (m.group (1))
        m = parameter_regex.match (line)
        if m:
            param_str = m.group (1)
            params_arr = param_str.split (',')
            out_line = current_subset + ' ' + \
                    str (current_temperature) + ' ' \
                    + ' '.join (params_arr) + '\n'
            out.write (out_line)
