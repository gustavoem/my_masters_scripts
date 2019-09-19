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
        model_idx = self.models.index (model)
        return [s for s in sample if s[0] == model_idx]

    def get_iteration_sample (self, sample, iteration):
        return [s for s in sample if s[1] == iteration]

    def get_n_sample_from_each_iteration (self, sample, n):
        ans = []
        current_it = sample[0][1]
        for i in range (len (sample)):
            if current_it == sample[i][1]:
                continue
            if current_it < sample[i][1]:
                back_idx = i - n - 1
                front_idx = i - 1
                ans += sample[back_idx:front_idx]
                current_it = sample[i][1]
        ans += sample[-n:]
        return ans

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


data_file = sys.argv[1]
# Process data
f = open (data_file, 'r')
sample_obj = FullSample ()
for line in f:
    v = line.split ()
    if v[0].isdigit ():
        model = int (v[0])
        iteration = float (v[1])
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
all_temperature = sample_obj.get_all_iterations ()
for model in models:
    sbml = SBML ()
    sbml.load_file (model + '.xml')
    odes = sbml_to_odes (sbml)
    odes.print_equations ()
    print ("Model: " + model)
    
    model_sample = sample_obj.get_model_sample (all_sample, model)
    for temp in all_temperature:
        print ("Temperature: " + str (temp))
        sample = sample_obj.get_iteration_sample (model_sample, temp)
        sample_size = min (50, len (sample))
        sample_idx = np.random.choice (range (len (sample)), 
                sample_size, replace=False)
        sub_sample = [sample[i] for i in sample_idx]
        temp_simulations = []
        for obs in sub_sample:
            # print (obs[:2])
            for i in range (len (param_odes_names[model])):
                p_name = param_odes_names[model][i]
                p_value = obs[2 + i]
                odes.define_parameter (p_name, p_value)
                # print (p_name + " = " + str (p_value))
            simulation = odes.evaluate_exp_on (experiment_measure, 
                    experiment_times)
            temp_simulations.append (simulation)
        simulation_data[model].append ((temp, temp_simulations))
        


# Plot simulations!
all_iterations = sample_obj.get_all_iterations () 
model_num = 0
for model in models:
    n_time = len (experiment_times)
    model_num += 1
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
                '{:0.3e}'.format (temp) + ' of model ' + str (model_num)
        plot_simulations_mean (plot_title, experiment_measure, 
                experiment_observations, sim_mean, sim_std, 
                experiment_times, figname)


        plot_title = 'All simulations of temperature ' + \
                '{:0.3e}'.format (temp) + ' of model ' + str (model_num)
        figname = 'msimulations_' + model + '_' + str (j) + '.png'
        plot_title = 'Simulations of temp. ' + \
                '{:0.2e}'.format (temp) + ' of model ' + str (model_num)
        plot_multiple_simulations (plot_title, experiment_measure, 
                experiment_observations, simulations,experiment_times, 
                figname)
