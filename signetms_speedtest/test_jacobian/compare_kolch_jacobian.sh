#!/bin/sh

# To run this you will need two branches of SigNetMS. One that 
# has no jacobian and one that has the jacobian

# First, change to master
cd ~/cs/SigNetMS && git checkout kolch && cd -

# Run without jacobian
python3 ../test_kolch/avg_time_kolch.py ~/cs/SigNetMS/input/Kolch/model1.xml ~/cs/SigNetMS/input/Kolch/model.priors ~/cs/SigNetMS/input/Kolch/small_experiment.data 10 10 > kolch_no_jacobian.txt

# Then change to jacobian branch
cd ~/cs/SigNetMS && git checkout kolch_jacobian && cd -

# Then run again with jacobian
python3 ../test_kolch/avg_time_kolch.py ~/cs/SigNetMS/input/Kolch/model1.xml ~/cs/SigNetMS/input/Kolch/model.priors ~/cs/SigNetMS/input/Kolch/small_experiment.data 10 10 > kolch_jacobian.txt
