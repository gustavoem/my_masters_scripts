import sys
sys.path.insert (0, '/home/gestrela/SigNetMS/.')
sys.path.insert (0, '/home/gustavo/cs/SigNetMS/.')

from model.SBML import SBML
from model.SBMLtoODES import sbml_to_odes
from marginal_likelihood.MarginalLikelihood import MarginalLikelihood
from model.PriorsReader import define_sbml_params_priors
from experiment.ExperimentSet import ExperimentSet
from marginal_likelihood.samplers.AcceptingRateAMCMC \
        import AcceptingRateAMCMC
from marginal_likelihood.samplers.PopulationalMCMC \
        import PopulationalMCMC
from parallel_map import parallel_map
from test_speed import get_exec_time 
import argparse
import time

parser = argparse.ArgumentParser ()
parser.add_argument ("model", help="SBLM file with mode definition.")
parser.add_argument ("priors", help="An XML file with the priors " \
        + "for the model parameters.")
parser.add_argument ("experiment", help="An XML file with the" \
        + " experiments observations.")
parser.add_argument ('repetitions', type=int, help="Number of  " \
        + "repetitions.")
args = parser.parse_args ()

sbml_file = args.model
priors_file = args.priors
experiment_file = args.experiment
repetitions = args.repetitions

sbml = SBML ()
sbml.load_file (sbml_file)
odes = sbml_to_odes (sbml)
experiments = ExperimentSet (experiment_file)
theta_priors = define_sbml_params_priors (sbml, priors_file)

n_process = 24
#iterations_schedule = [250, 500, 1000, 2000]
iterations_schedule = [1, 10, 100, 200, 400]
# iterations_schedule = [1, 10, 20]
#iterations_schedule = [20, 40]
for n_iterations in iterations_schedule:
    total_time = 0
    for _ in range (repetitions):
        print ("iteration - ", _, "done!")
        total_time += get_exec_time (odes, experiments, theta_priors, \
                n_iterations, n_process)
    avg_time = total_time / float (repetitions)
    print ("Integrating", n_iterations, "times, we got average time of " \
            + "{:.3f}".format (avg_time))
