import matplotlib
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import numpy as np

data_file = sys.argv[1]

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
    
    def add_model (self, model_name, parameters):
        self.models.append (model_name)
        self.model_params[model_name] = parameters

    def get_all_models (self):
        return self.models

    def get_model_params (self, model):
        return self.model_params[model]


def plot_parameter_distribution (plot_title, param_sample, param_name, 
        fig_name, extra_tick=None):
    x = np.array (param_sample)
    tex_param_name = '$' + param_name + '$'
    plt.title (plot_title)
    plt.ylabel ('Estimated $p (' + param_name + '|M, D)$')
    plt.xlabel ('Paramater value')
    
    try:
        sns_plot = sns.distplot (x, label=tex_param_name, hist=False, 
            rug=True)
    except:
        return
    fig = sns_plot.get_figure ()
    
    # Add parameter to the ticks
    # Must draw the canvas to position the ticks
    fig.canvas.draw()
    if extra_tick is not None:
        locs, labels = plt.xticks ()
        locs = list (locs) + [extra_tick]
        labels += [tex_param_name]
        plt.xticks (locs, labels)
        _, labels = plt.xticks ()
        my_label = labels[-1]
        _, position_y = my_label.get_position ()
        my_label.set_y (position_y - .05)

    plt.tight_layout ()
    fig.savefig (fig_name, transparent=True)
    plt.clf ()

param_original_value = [0.07, 0.6, 0.05, 0.3, 0.017, 0.3]

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
        
# Plot data
all_models = sample_obj.get_all_models ()
all_temp = sample_obj.get_all_iterations ()
full_sample = sample_obj.get_full_sample ()

for model in all_models:
    print ("Ploting parameters of model " + model)
    parameters = sample_obj.get_model_params (model)
    sample = sample_obj.get_model_sample (full_sample, model)
    model_idx = all_models.index (model)
    
    for i in range (len (all_temp)):
        temp = all_temp[i]
        print ("Plotting parameters with temperature " + str (temp))
        t_sample = sample_obj.get_iteration_sample (sample, temp)

        if t_sample == []:
            continue

        for p in parameters:
            p_idx = parameters.index (p)
            param_sample = [obs[2 + p_idx] for obs in t_sample]
            fig_name = model + '_' + str (i) + '_p' + \
                    str (p_idx) + '_' + p + '.png'
            extra_tick = None
            if model == 'model1':
                extra_tick = param_original_value[p_idx]
            
            plot_title = 'Posterior of temp. ' + \
                    '{:0.2e}'.format (temp) + ' of parameter $' + p + \
                    '$ of model ' + str (model_idx + 1)
            plot_parameter_distribution (plot_title, param_sample, p, 
                fig_name, extra_tick)
