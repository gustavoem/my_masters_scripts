import sys
SigNetMS_path = '/home/gustavo/cs/SigNetMS'
sys.path.insert (0, SigNetMS_path)

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from marginal_likelihood.ODES import ODES
from marginal_likelihood.SBML import SBML
from marginal_likelihood.SBMLtoODES import sbml_to_odes
from marginal_likelihood.RandomParameterList import RandomParameterList
from experiment.ExperimentSet import ExperimentSet

class FullSample:

    def __init__ (self):
        self.data = []
        self.models = []
        self.model_params = {}

    def add_data (self, d):
        self.data.append (d)
    
    def get_full_sample (self):
        return list (self.data)
    
    def get_model_sample (self, sample, model):
        model_idx = self.models.index (model)
        return [s for s in sample if s[0] == model_idx]

    def get_iteration_sample (self, sample, iteration):
        return [s for s in sample if s[1] == iteration]

    def add_model (self, model_name, parameters):
        self.models.append (model_name)
        self.model_params[model_name] = parameters

    def get_all_models (self):
        return self.models

    def get_model_params (self, model):
        return self.model_params[model]


def plot_simulations (plot_title, exp_measure, exp_observations, 
        sim_mean, sim_std, times, figname):
    fig, ax = plt.subplots()
    
    # plot experiments
    i = 1
    for obs in exp_observations:
        label = 'Experimental observation #' + str (i)
        ax.plot(times, obs, label=label)
        i += 1

    plt.title (plot_title)
    plt.ylabel ('$' + exp_measure + '$')
    plt.xlabel ('Time')
    plt.errorbar (times, sim_mean, sim_std, 
            label='Simulated observations')
    ax.legend ()
    fig.savefig (figname)
    plt.clf ()


data_file = sys.argv[1]
# Process data
f = open (data_file, 'r')
sample_obj = FullSample ()
for line in f:
    v = line.split ()
    if v[0].isdigit ():
        model = int (v[0])
        iteration = int (v[1])
        data = [model, iteration]
        data += [float (p) for p in v[2:]]
        sample_obj.add_data (data)
    else:
        model_name = v[0]
        parameters = v[1:]
        sample_obj.add_model (model_name, parameters)

print ("All models: " + str (sample_obj.get_all_models ()))
param_odes_names = {
        'model1': ['p1', 'p2', 'p3', 'p4', 'p5', 'p6'],
        'model2': ['p1', 'p2', 'p3', 'p4', 'p5'],
        'model3': ['p1', 'p2', 'p3', 'p4'],
        'model4': ['p1', 'p2', 'p3', 'p4', 'p5', 'p6', 'p7']
}

experiment_file = 'experiment.data'
exp_set = ExperimentSet (experiment_file)
models = sample_obj.get_all_models ()

# Experiment data
experiment_observations = []
experiment_times = exp_set[-1].times
experiment_measure = exp_set[-1].measure_expression
for exp in exp_set:
    obs = exp.values 
    experiment_observations.append (obs)

# Simulation data
simulation_data = {m: [] for m in models}

all_sample = sample_obj.get_full_sample ()
for model in models:
    sbml = SBML ()
    sbml.load_file (model + '.xml')
    odes = sbml_to_odes (sbml)
    # print ("Model " + model + " has equations: ")
    odes.print_equations ()
    
    model_sample = sample_obj.get_model_sample (all_sample, model)
    
    # if model == 'model1':
        # model_sample.insert (0, [0, 1, 0.07, 0.6, 0.05, 0.3, 0.017, 
            # 0.3])

    for obs in model_sample:
        for i in range (len (param_odes_names[model])):
            p_name = param_odes_names[model][i]
            p_value = obs[2 + i]
            odes.define_parameter (p_name, p_value)
        simulation = odes.evaluate_exp_on (experiment_measure, 
                experiment_times)
        simulation_data[model].append (simulation)


# Plot simulations!
for model in models:
    t = len (experiment_times)
    simulations = np.array (simulation_data[model])
    sim_mean = [np.mean (simulations[:, i]) for i in range (t)]
    sim_std = [np.std (simulations[:, i]) for i in range (t)]
    figname = 'simulations_' + model + '.png'
    plot_title = ''
    plot_simulations (plot_title, experiment_measure, 
            experiment_observations, sim_mean, sim_std, 
            experiment_times, figname)
