import sys
SigNetMS_path = '/home/gustavo/cs/SigNetMS'
sys.path.insert (0, SigNetMS_path)

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from model.ODES import ODES
from model.SBML import SBML
from model.SBMLtoODES import sbml_to_odes
from model.RandomParameterList import RandomParameterList
from experiment.ExperimentSet import ExperimentSet

class FullSample:

    def __init__ (self):
        self.data = []
        self.models = []
        self.model_params = {}
        self.iterations = []

    def add_data (self, d):
        self.data.append (d)
        data_t = d[1]
        if data_t not in self.iterations:
            self.iterations.append (data_t)

    def get_all_iterations (self):
        return self.iterations
    
    def get_full_sample (self):
        return list (self.data)
    
    def get_model_sample (self, sample, model):
        return [s for s in sample if s[0] == model]

    def get_iteration_sample (self, sample, iteration):
        return [s for s in sample if s[1] == iteration]

    def add_model (self, model_name, parameters):
        self.models.append (model_name)
        self.model_params[model_name] = parameters

    def get_all_models (self):
        return self.models

    def get_model_params (self, model):
        return self.model_params[model]


def plot_multiple_simulations (plot_title, exp_measure, 
        exp_observations, sims, times, figname):
    fig, ax = plt.subplots()
    
    # plot experiments
    i = 1
    for obs in exp_observations:
        label = 'Experimental observation #' + str (i)
        ax.plot(times, obs, label=label)
        i += 1

    # i = 1
    ax.plot (times, sims[0], c=(1, 0.25, 0.25, 0.3), 
            label='Simulated observation')
    for sim in sims[1:]:
        ax.plot (times, sim, c=(1, 0.25, 0.25, 0.3))

    plt.title (plot_title)
    plt.ylabel ('$[' + exp_measure + ']$')
    plt.xlabel ('Time (s)')
    ax.legend ()
    fig.savefig (figname, transparent=True)
    plt.clf ()


def plot_simulations_mean (plot_title, exp_measure, exp_observations, 
        sim_mean, sim_std, times, figname):
    fig, ax = plt.subplots()
    
    # plot experiments
    i = 1
    for obs in exp_observations:
        label = 'Experimental observation #' + str (i)
        ax.plot(times, obs, label=label)
        i += 1

    plt.title (plot_title)
    plt.ylabel ('$[' + exp_measure + ']$')
    plt.xlabel ('Time (s)')
    plt.errorbar (times, sim_mean, sim_std, 
            label='Simulated observations')
    ax.legend ()
    fig.savefig (figname, transparent=True)
    plt.clf ()


def isfloat (string):
    try:
        float (string)
        return True
    except ValueError:
        return False


data_file = sys.argv[1]
# Process data
f = open (data_file, 'r')
sample_obj = FullSample ()
for line in f:
    v = line.split ()
    if isfloat (v[1]):
        model = v[0]
        iteration = float (v[1])
        data = [model, iteration]
        data += [float (p) for p in v[2:]]
        sample_obj.add_data (data)
    else:
        model_name = v[0]
        parameters = v[1:]
        sample_obj.add_model (model_name, parameters)

print ("All models:\n", '\n'.join (sample_obj.get_all_models ()))
experiment_file = 'gauss_noise.data'
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
all_temperature = sample_obj.get_all_iterations ()
for model in models:
    sbml = SBML ()
    sbml.load_file (model + '/model.sbml')
    odes = sbml_to_odes (sbml)
    odes.print_equations ()
    print ("Model: " + model)
    
    model_sample = sample_obj.get_model_sample (all_sample, model)
    for temp in all_temperature:
        print ("Temperature: " + str (temp))
        sample = sample_obj.get_iteration_sample (model_sample, temp)
        sample_size = min (10, len (sample))
        sample_idx = np.random.choice (range (len (sample)), 
                sample_size, replace=False)

        sub_sample = [sample[i] for i in sample_idx]
        temp_simulations = []
        for obs in sub_sample:
            n_params = len (sample_obj.get_model_params (model))
            for i in range (n_params):
                p_name = 'p' + str (i + 1)
                p_value = obs[2 + i]
                odes.define_parameter (p_name, p_value)
            simulation = odes.evaluate_exp_on (experiment_measure, 
                    experiment_times)
            temp_simulations.append (simulation)
        simulation_data[model].append ((temp, temp_simulations))
        


# Plot simulations!
all_iterations = sample_obj.get_all_iterations () 
for model in models:
    n_time = len (experiment_times)
    for j in range (len (simulation_data[model])):
        temp, simulations = simulation_data[model][j]
        if simulations == []:
            continue

        simulations = np.array (simulations)
        sim_mean = [np.mean (simulations[:, i]) for i in range (n_time)]
        sim_std = [np.std (simulations[:, i]) for i in range (n_time)]
    
        figname = 'simulations_' + model + '_' + str (j) + \
                '.png'
        plot_title = 'Avg. simulations of temperature ' + \
                '{:0.3e}'.format (temp) + ' of ' + str (model)
        plot_simulations_mean (plot_title, experiment_measure, 
                experiment_observations, sim_mean, sim_std, 
                experiment_times, figname)


        plot_title = 'All simulations of temperature ' + \
                '{:0.3e}'.format (temp) + ' of ' + str (model)
        figname = 'msimulations_' + model + '_' + str (j) + '.png'
        plot_title = 'Simulations of temp. ' + \
                '{:0.2e}'.format (temp) + ' of ' + str (model)
        plot_multiple_simulations (plot_title, experiment_measure, 
                experiment_observations, simulations,experiment_times, 
                figname)
