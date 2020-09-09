#!/bin/sh

# change to sympy_autowrap branch
#cd ~/cs/SigNetMS && git checkout sympy_autowrap && cd -
# Then run again
#python3 avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 11 > autowrap.txt

# change to string evaluation
cd ~/cs/SigNetMS && git checkout 042701af63545cd64c3cc3831dcae97901547865 && cd -

# Run with string evaluation
python3 avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 11 > string_eval.txt

# Then change to sympy_system branch
#cd ~/cs/SigNetMS && git checkout sympy_system && cd -
# Then run again
#python3 avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 11 > lambdify.txt

# Then change to sympy_system_jac branch
cd ~/cs/SigNetMS && git checkout sympy_system_jac && cd -
# Then run again
python3 avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 11 > lambdify_jac.txt


