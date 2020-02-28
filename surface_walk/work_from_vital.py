from pathlib import Path
SIGNET_MS_PATH =  '/project/msreis/modelSelection/project/SigNetMS'
CURRENT_PATH = str (Path ().absolute ())
import sys
sys.path.insert (0, SIGNET_MS_PATH)

from SigNetMS import perform_marginal_likelihood


def calculate_score (subset_directory):
    """ Given the subset of a model, calculates the score of this model. 
    """
    subset_dir_path = CURRENT_PATH + '/' + subset_directory
    model_file = subset_dir_path + '/model.sbml'
    priors_file = subset_dir_path + '/model.priors'
    sample_file = subset_dir_path + '/sample.txt'
    exp_file = CURRENT_PATH + '/gauss_noise.data'
    try:
        score = perform_marginal_likelihood (model_file, priors_file, \
                exp_file, 15000, 1000, 3000, 1000, n_process=24,\
                sample_output_file=sample_file)
    except ValueError:
        print ("There was no convergence of parameters in burn-in" \
                + " sampling.")
        score = None
    except Exception as e:
        print ("Something else happened")
        print (e)
        score = None
    return score


starting_model = int (sys.argv[1])

all_subsets = [
    "subset_11111000000000000000000",
    "subset_11111000000000100000000",
    "subset_11111000000000100000001",
    "subset_11111000000000110000001",
    "subset_11111100000001110000001",
    "subset_11111100010001110000001",
    "subset_11111100010001110001001",
    "subset_11111101010001110001001",
    "subset_11111101010001110011001",
    "subset_11111101010001110011011",
    "subset_11111101110001110011011",
    "subset_11111101111001110011011",
    "subset_11111101111001110111011",
    "subset_11111101111011110111011",
    "subset_11111101111011110111111",
    "subset_11111111111011110111111",
    "subset_11111111111011111111111",
    "subset_11111111111111111111111"]

subset_and_scores = []
for i in range (starting_model, len (all_subsets)):
    subset = all_subsets[i]
    score = calculate_score (subset)
    subset_and_scores.append ((subset, score))
    print ("Completed sampling of", subset)

for subset, score in subset_and_scores:
    print (subset +  ":", score )
