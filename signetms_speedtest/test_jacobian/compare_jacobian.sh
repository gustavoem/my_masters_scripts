#!/bin/sh

# hmm... to run this you will need two branches of SigNetMS. One that 
# has no jacobian and one that has the jacobian

# First, change to master
cd ~/cs/SigNetMS && git checkout master && cd -

# Run without jacobian
python3 ../avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 100 50 > no_jacobian.txt

# Then change to jacobian branch
cd ~/cs/SigNetMS && git checkout jacobian_again && cd -

# Then run again with jacobian
python3 ../avg_time.py ~/cs/SigNetMS/input/bioinformatics/model1.xml ~/cs/SigNetMS/input/bioinformatics/model.priors ~/cs/SigNetMS/input/bioinformatics/experiment.data 100 50 > jacobian.txt
