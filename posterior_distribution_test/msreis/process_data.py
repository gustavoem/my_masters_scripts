from pathlib import Path
SIGNET_MS_PATH =  '/project/msreis/modelSelection/project/SigNetMS'
CURRENT_PATH = str (Path ().absolute ())

import os
import sys
sys.path.insert (0, SIGNET_MS_PATH)
from model.SBML import SBML
from model.PriorsReader import define_sbml_params_priors


subdirs = [subdir[0] for subdir in os.walk (CURRENT_PATH)]
model_dirs = [subdir for subdir in subdirs if 'subset' in subdir]
print ('\n'.join (model_dirs))

model_params = {}
for model_dir in model_dirs:
    priors_file = model_dir + '/model.priors'
    model_file = model_dir + '/model.sbml'
    model_sbml = SBML ()
    model_sbml.load_file (model_file)
    theta_priors = define_sbml_params_priors (model_sbml, priors_file)
    param_names = [] 
    for p in theta_priors:
        param_names.append (p.name)
    model_params[model_dir
