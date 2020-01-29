"""Roads only accessible to humans experiment.

Simulates road experiment where humans infected or not can change from place
using roads. We change the incubation_time to check if the spread, the
percentage of agent infected, is effected by it.
"""
import sys
sys.path.append("..")
import json
from p_tqdm import p_umap
import csv
import multiprocessing as mp
import time
import subprocess
import os
import random
import numpy as np
from model import Apocalypse



def make_params():
    """Set the model parameters to use in the experiments."""
    simulation_start = 0
    simulation_end = 1000
    simulation_stepsize = 1

    inc_time_start = 0
    inc_time_end = 18
    inc_time_stepsize = 2

    inc_times = np.arange(inc_time_start, inc_time_end, inc_time_stepsize)
    simulations = np.arange(simulation_start, simulation_end,
                            simulation_stepsize)

    return inc_times, simulations


def get_model_params():
    """Standard parameters of the model in all experiments."""
    return {
        "width": 30,
        "height": 30,
        "density": 0.25,
        "infected_chance": 0.05,
        "incubation_time": None,
        "map_id": 0,
        "human_kill_agent_chance": 0.35
    }


def make_models(inc_times, simulations):
    """Make model for each experiment."""
    models = []

    for incubation_time in inc_times:
        for _ in simulations:
            # Fix simulations iterator after updating
            # the unfinished experiment
            model = get_model_params()
            model["incubation_time"] = incubation_time
            model["seed"] = str(random.randrange(sys.maxsize))
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
    series = []
    it = 0
    while True:
        it += 1
        model.step()
        series.append((model.susceptible, model.infected, model.carrier,
                       model.recovered))
        if (model.infected == 0 and model.carrier == 0) or \
                (model.susceptible == 0):
            return {"data": series, "density": str(params["density"]),
                    "incubation_time": str(params["incubation_time"])}
        # Zombies win
        if it > 200:
            return {"data": series, "density": str(params["density"]),
                    "incubation_time": str(params["incubation_time"])}


def run_experiment(models, series_file):
    """Run experiment on multiple cores and write result to series_file."""
    results = p_umap(run_simulation, models)
    print("time for writing the results")
    with open(series_file, "w") as file:
        file.write(json.dumps(results))


if __name__ == "__main__":
    os.environ["mode"] = "5"
    inc_times, simulations = make_params()
    models = make_models(inc_times, simulations)
    write_models(models, "roads_models.csv")
    run_experiment(models, "road_series.json")
