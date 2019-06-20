#!/bin/sh

# First run intel_python
/home/gestrela/cs/intelpython3/pkgs/python-3.6.8-7/bin/python3.6 avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 100 50 > inte_python_results.txt
# Then run python
python3 avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 100 50 > cpython_results.txt
