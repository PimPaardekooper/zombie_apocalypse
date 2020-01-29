"""Main experiment.

Experiment on a 30x30 grid, where we change the population density and the
incubation time and see how many times of all experiments the humans win.
We do this then for humans wo use herding and humans wo do not.
"""
import sys
sys.path.append("..")
from model import Apocalypse
import os
import numpy as np
import random
import csv
from p_tqdm import p_umap


def make_params():
    """Set the model parameters to use in the experiments."""
    density_stepsize = 0.1
    density_start = 0.05
    density_end = 0.5
    densities = np.arange(density_start, density_end, density_stepsize)

    simulation_start = 0
    simulation_end = 10
    simulation_stepsize = 1
    simulations = np.arange(simulation_start, simulation_end,
                            simulation_stepsize)

    return densities, simulations

def get_model_params(group):
    """Standard parameters of the model in all experiments."""
    return {
        "width": 50,
        "height": 50,
        "density": None,
        "infected_chance": 0.05,
        "map_id": 0,
        "grouping": group,
        "human_kill_agent_chance": 0.35
    }

def make_models(inc_times, simulations, group):
    """Make model for each experiment."""
    models = []

    for density in densities:
        for iteration in simulations:
            # Fix simulations iterator after updating
            # the unfinished experiment
            model = get_model_params(group)
            model["density"] = density
            model["grouping"] = group
            model["seed"] = str(random.randrange(sys.maxsize))
            model["iteration"] = iteration
            models.append(model)

    return models

def write_models(models, model_file):
    """Write models made to model_file."""
    with open(model_file, 'w', newline="") as csv_file:
        writer = csv.writer(csv_file)
        for model in models:
            writer.writerow(model.values())

def run_simulation(params):
    """Run experiment with given parameters. Return outcome of experiment."""
    model = Apocalypse(**params)

    while True:
        model.step()

        # Zombies win
        if model.susceptible == 0:
            params['winner'] = 'zombies'
            params['steps'] = model.schedule.steps
            return params

        # Humans win
        elif model.infected == 0 and model.carrier == 0:
            params['winner'] = 'human'
            params['steps'] = model.schedule.steps
            return params

def run_experiment(models, series_file):
    """Run experiment on multiple cores and write result to series_file."""
    results = p_umap(run_simulation, models)
    print("time for writing the results")
    with open(series_file, "a") as file:
        for result in results:
            file.write('{:.2f},{:d},{:d},{:},{:},{:d}\n'.format(
                result["density"], int(result["grouping"]), int(result["iteration"]),
                result["seed"], result["winner"], result["steps"]
            ))


if __name__ == "__main__":
    os.environ["mode"] = "3"

    for group in [True, False]:
        if group:
            output_file = "density_and_incubation_grouping.csv"
        else:
            output_file = "density_and_incubation_nogrouping.csv"

        densities, simulations = make_params()
        models = make_models(densities, simulations, group)
        write_models(models, "group_models.csv")
        run_experiment(models, output_file)