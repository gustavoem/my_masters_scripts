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
import re
import json

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

    plt.ylim(790, 820)
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

def plot_experiments(exp_observations, exp_measure, times):
    fig, ax = plt.subplots()
    
    # plot experiments
    i = 1
    for obs in exp_observations:
        label = 'Experimental observation #' + str (i)
        ax.plot(times, obs, label=label)
        i += 1

    plt.title ('Artificial Experimental Data')
    plt.ylabel ('$[' + exp_measure + ']$')
    plt.xlabel ('Time (s)')
    ax.legend ()
    fig.savefig ('experiment_plot.pdf', transparent=True)
    plt.clf ()


model_file = None
sample_file = None
if len(sys.argv) > 2:
    model_file = sys.argv[1]
    sample_file = sys.argv[2]
# Process data
sample = []
temperatures = []

f = open (sample_file, 'r')
# Sample for t = 0.5776399743931226
# parameter = [1.5, 618.2] likelihood = -192.2
for line in f:
    temperature_regex = r"Sample for t = (\d+\.\d+)"
    sample_regex = r"parameter = (\[[\d+\.\d+,?\s?]+\])"
    m = re.match(temperature_regex, line)
    if m:
        temperatures.append(float(m.group(1)))
    m = re.match(sample_regex, line)
    if m:
        if len(sample) < len(temperatures):
            sample.append([])
        theta = json.loads(m.group(1))
        sample[-1].append(theta)

experiment_file = 'experiment.data'
exp_set = ExperimentSet (experiment_file)

# Experiment data
experiment_observations = []
experiment_times = exp_set[-1].times
experiment_measure = exp_set[-1].measure_expression
for exp in exp_set:
    obs = exp.values 
    experiment_observations.append (obs)

plot_experiments(
    experiment_observations,
    experiment_measure,
    experiment_times
)

if model_file is None:
    sys.exit(0)

# Simulation data
sbml = SBML ()
sbml.load_file (model_file)
odes = sbml_to_odes (sbml)
odes.print_equations ()
model_name = sbml.get_name()
print ("Model: " + model_name)

sbml_params = sbml.get_all_param()

simulation_data = []
for i, temp in enumerate(temperatures):
    print ("Temperature: " + str (temp))
    temp_sample = sample[i]
    print ("sample size = " + str (len(temp_sample)))
    sample_size = min (50, len (temp_sample))
    sample_idx = np.random.choice(
        range(len(temp_sample)), 
        sample_size,
        replace=False
    )
    sub_sample = [temp_sample[i] for i in sample_idx]
    temp_simulations = []
    for obs in sub_sample:
        # print (obs[:2])
        for i, p_name in enumerate(sbml_params):
            p_value = obs[i]
            odes.define_parameter (p_name, p_value)
            # print (p_name + " = " + str (p_value))
        simulation = odes.evaluate_exp_on(
            experiment_measure, 
            experiment_times
        )
        # print(simulation)
        temp_simulations.append (simulation)
    simulation_data.append((temp, temp_simulations))
        
# Plot simulations!
n_time = len(experiment_times)
temp_i = 0
for j in range(len(simulation_data)):
    temp, simulations = simulation_data[j]
    if simulations == []:
        continue
    print('Plotting temperature = ', temp)

    simulations = np.array (simulations)
    sim_mean = [np.mean (simulations[:, i]) for i in range (n_time)]
    sim_std = [np.std (simulations[:, i]) for i in range (n_time)]

    figname = 'simulations_' + model_name + '_' + str(temp_i) + '.pdf'
    plot_title = 'Avg. simulations with beta = ' + \
            '{:0.3e}'.format (temp) + ' of ' + model_name
    plot_simulations_mean(
        plot_title,
        experiment_measure,
        experiment_observations,
        sim_mean,
        sim_std, 
        experiment_times,
        figname
    )

    figname = 'msimulations_' + model_name + '_' + str(temp_i)  + '.pdf'
    plot_title = 'Simulations with beta = ' + \
            '{:0.2e}'.format (temp) + ' of ' + model_name
    plot_multiple_simulations(
        plot_title,
        experiment_measure, 
        experiment_observations,
        simulations,experiment_times, 
        figname
    )
    temp_i += 1
