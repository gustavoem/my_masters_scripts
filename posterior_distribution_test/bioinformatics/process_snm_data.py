import os 
import re

models = ['model1', 'model2', 'model3', 'model4']
parameters = {'model1': ['compartment', 'k_1', 'k_2', 'k_3', 'k_4', 'V', 
    'K_m'],
    'model2': ['compartment', 'k_1', 'V_1', 'k_2', 'k_3', 'V_2'],
    'model3': ['compartment', 'V_1', 'k_1', 'V_2', 'k_2'],
    'model4': ['compartment', 'k_1', 'k_2', 'k_3', 'k_4', 'k_5', 'k_6', 
        'k_7']
}

output_file = 'bioinformatics_snm_results.txt'
out = open (output_file, 'w')

current_dir = os.getcwd ()
pop_temp_regex = re.compile ("Sample for t = " + \
        "(\d*\.\d+(?:e(?:\-|\+)\d+)?)")
parameter_regex = re.compile ("parameter = \[(.*)\]")

# First line of the output is the header:
# model1_name parameters_of_the_model1
# model2_name parameters_of_the_model2
# ...
# modelm_name parameters_of_the_modelm
for m in models:
    line = m + ' ' + ' '.join (parameters[m][1:]) + '\n'
    out.write (line)

for i in range (len (models)):
    file_name = 'tail_girolami_' + str (i + 1) + '.txt'
    try:
        f = open (file_name)
    except:
        print ("Could not open " + file_name)


    current_temperature = 0 
    for line in f:
        m = pop_temp_regex.match (line)
        if m:
            current_temperature = float (m.group (1))
        m = parameter_regex.match (line)
        if m:
            param_str = m.group (1)
            params_arr = param_str.split (',')
            out_line = str (i) + ' ' + str (current_temperature) + \
                    ' ' + ' '.join (params_arr) + '\n'
            out.write (out_line)
