import sys
sys.path.insert (0, '/home/gestrela/cs/SigNetMS/.')

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
import argparse
import time

def run_sampler (temp, ode, experiments, theta_priors, iterations):
    acc_mcmc = AcceptingRateAMCMC (theta_priors, ode, experiments, \
            iterations, verbose=False)
    acc_mcmc.set_temperature (temp)
    acc_mcmc.start_sample_from_prior ()
    acc_mcmc.get_sample (iterations)


def get_exec_time (odes, experiments, theta_priors, n_iterations, \
        nof_process):
    start_time = time.time ()
    # initialize ODEs function and jacobian
    odes.evaluate_on ([experiments[0].times[0]])
    odes.get_system_jacobian ()

    temperatures = PopulationalMCMC.sample_scheduled_betas (20)
    sample_runner = lambda temp : run_sampler (temp, odes, \
            experiments, theta_priors, n_iterations)
    parallel_map (sample_runner, temperatures, nof_process)

    elapsed_time = time.time () - start_time
    return elapsed_time


if __name__ == "__main__":
    parser = argparse.ArgumentParser ()
    parser.add_argument ("model", help="SBLM file with model " \
            + "definition.")
    parser.add_argument ("priors", help="An XML file with the priors " \
            + "for the model parameters.")
    parser.add_argument ("experiment", help="An XML file with the" \
            + " experiments observations.")
    parser.add_argument ("iterations", help="How many" \
            + " iterations should be performed to test speed.")
    parser.add_argument ('--n_process', type=int, nargs='?', \
            default=0, help="Number of parallel process used on " \
            + "sampling step.")
    args = parser.parse_args ()

    # Problem input
    sbml_file = args.model
    priors_file = args.priors
    experiment_file = args.experiment

    # Algorithm parameters
    n_iterations = int (args.iterations)
    nof_process = args.n_process

    print ("Performing sampling speed test on model: " + sbml_file)
    print ("Using " + str (nof_process) + " process to sample in " + \
            "20 different temperatures.")

    sbml = SBML ()
    sbml.load_file (sbml_file)
    odes = sbml_to_odes (sbml)
    experiments = ExperimentSet (experiment_file)
    theta_priors = define_sbml_params_priors (sbml, priors_file)
    elapsed_time = get_exec_time (odes, experiments, theta_priors, \
            n_iterations, nof_process)
    print ("Time elapsed: " + "{:.3f}".format(elapsed_time) + \
            " seconds.")

