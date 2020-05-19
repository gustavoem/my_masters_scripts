from pathlib import Path
SIGNET_MS_PATH =  '/home/gestrela/SigNetMS'
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
                exp_file, 10000, 1000, 3000, 1000, n_process=24,\
                sample_output_file=sample_file, seed=42)
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
        "subset_10000000011001100000000",
        "subset_10000000011001101000000",
        "subset_10000000011001101000100",
        "subset_10000000011101101000100",
        "subset_10000000011101111000100",
        "subset_10000000011101111000101",
        "subset_10000000011111111000101", # optimal
        "subset_10000100011111111000101", 
        "subset_10000100011111111100101",
        "subset_10000101011111111100101",
        "subset_10001101011111111100101",
        "subset_10011101011111111100101",
        "subset_10011111011111111100101",
        "subset_10111111011111111100101",
        "subset_11111111011111111100101",
        "subset_11111111011111111101101",
        "subset_11111111011111111101111",
        "subset_11111111111111111101111",
        "subset_11111111111111111111111"
]

scores_file = open('work_from_scores.txt', 'w')

subset_and_scores = []
for i in range (starting_model, len (all_subsets)):
    subset = all_subsets[i]
    score = calculate_score (subset)
    scores_file.write(subset + ': ' + str (score) + '\n')
    subset_and_scores.append ((subset, score))
    print ("Completed sampling of", subset)

scores_file.close ()

for subset, score in subset_and_scores:
    print (subset +  ":", score )
