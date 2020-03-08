#!/bin/bash
SIGNET_MS_PATH="/home/gestrela/cs/SigNetMS"

source /home/gestrela/signetms_env/bin/activate 
python ../avg_time.py $SIGNET_MS_PATH/input/bioinformatics/model1.xml \
  $SIGNET_MS_PATH/input/bioinformatics/model.priors \
  $SIGNET_MS_PATH/input/bioinformatics/experiment.data 2000 50 > result_again2.txt
