#!/bin/sh

# change to sympy_autowrap branch
cd ~/cs/SigNetMS && git checkout sympy_autowrap && cd -
# Then run again
python3 avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 50 > autowrap.txt

# change to master
cd ~/cs/SigNetMS && git checkout master && cd -

# Run master
python3 avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 50 > master.txt

# Then change to sympy_system branch
cd ~/cs/SigNetMS && git checkout sympy_system && cd -
# Then run again
python3 avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 50 > lambdify.txt

# Then change to sympy_system_jac branch
cd ~/cs/SigNetMS && git checkout sympy_system_jac && cd -
# Then run again
python3 avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 50 > lambdify_jac.txt


