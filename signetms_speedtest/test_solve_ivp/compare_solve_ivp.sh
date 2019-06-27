#!/bin/sh

# hmm... to run this you will need two branches of SigNetMS. One that 
# has no jacobian and one that has the jacobian

# First, change to master
cd ~/cs/SigNetMS && git checkout master && cd -

# Run master
python3 ../avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 20 50 > master.txt

# Then change to scipy_solve_ivp branch
cd ~/cs/SigNetMS && git checkout scipy_solve_ivp && cd -

# Then run again
python3 ../avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 20 50 > solve_ivp.txt

# Then change to scipy_solve_ivp_jac branch
cd ~/cs/SigNetMS && git checkout scipy_solve_ivp_jac && cd -

# Then run again
python3 ../avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 20 50 > solve_ivp_jacobian.txt

