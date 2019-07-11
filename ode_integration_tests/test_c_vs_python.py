import sys
import time
import statistics
import os
from subprocess import Popen


implementation = ['c', 'py_odeint', 'py_vode', 'py_asteval_odeint']
extension = {'c': '.c', 
        'py_odeint': '.py',
        'py_vode': '.py',
        'py_asteval_odeint': '.py'}
run_command = {'c': './c/integrate',
        'py_odeint': 'python3 ./py_odeint/integrate.py',
        'py_asteval_odeint': 'python3 ./py_asteval_odeint/integrate.py',
        'py_vode': 'python3 ./py_vode/integrate.py'}
number_of_integrations = [20, 100, 500, 1000, 5000]

reps = int(sys.argv[1])
times = []
for n in number_of_integrations:
    print("Running implementations for n = " + str(n) + \
            " integrations.")
    times_on_n_integrations = {}
    for imp in implementation:
        times_on_n_integrations[imp] = []
        p = Popen(['/usr/bin/mpstat -P ALL 1 > cpu_usage_' + imp \
                    + '_' + str(n) + '.txt'], shell=True)
        for _ in range (reps):
            start = time.time()
            os.system(run_command[imp] + " " + str(n))
            end = time.time()
            times_on_n_integrations[imp].append(end - start)
        p.terminate()
    times.append(times_on_n_integrations)

out_file_name = '_'.join(implementation) + '.txt'
out_file = open(out_file_name, 'w')
for i in range(len(number_of_integrations)):
    line = str(number_of_integrations[i])
    times_on_n_integrations = times[i]
    for imp in implementation:
        times_of_imp = times_on_n_integrations[imp]
        avg = statistics.mean(times_of_imp)
        stddev = statistics.stdev(times_of_imp)
        line += "\t" + str(avg) + "±" + str(stddev)
    print(line + "\n")
    out_file.write(line + "\n")
