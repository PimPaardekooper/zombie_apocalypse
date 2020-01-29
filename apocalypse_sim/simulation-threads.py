"""Run the simulations over multiple threads."""

from model import Apocalypse
import numpy as np
import random
import sys
import os
import subprocess
import time
import multiprocessing as mp
import csv
from p_tqdm import p_umap


def read_last_line(filename):
    """Read last line."""
    a = subprocess.check_output(['tail', '-1', filename])[0:-1].decode('utf-8')
    return a


def delete_last_line(filename):
    """Delete last line."""
    subprocess.check_output(['sed', '-i', '$d', filename])


# Default parameters for iterators
density_stepsize = 0.1
inc_time_stepsize = 3
simulation_stepsize = 1

density_start = 0.05
inc_time_start = 0
simulation_start = 0

# Ends (exclusive)
density_end = 0.75
inc_time_end = 18
simulation_end = 25

# last_experiment = read_last_line(filename)
os.environ["mode"] = "3"


def get_model_params():
    """Get all parameters needed for the model."""
    return {
        "width": 30,
        "height": 30,
        "density": None,
        "infected_chance": 0.05,
        "incubation_time": None,
        "map_id": 0,
        "human_kill_agent_chance": 0.35,
        "grouping": False
    }


densities = np.arange(density_start, density_end, density_stepsize)
inc_times = np.arange(inc_time_start, inc_time_end, inc_time_stepsize)
simulations = np.arange(simulation_start, simulation_end, simulation_stepsize)

first = True


def run_simulation(params):
    """Run the simulation."""
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


models = []

for density in densities:
    for incubation_time in inc_times:
        for iteration in simulations:
            # Fix simulations iterator after updating
            # the unfinished experiment
            if first:
                simulations = np.arange(
                    0, simulation_end, simulation_stepsize
                )

            model = get_model_params()
            model["grouping"] = False
            model["density"] = density
            model["incubation_time"] = incubation_time
            model["seed"] = str(random.randrange(sys.maxsize))
            model["iteration"] = iteration

            models.append(model)

with open('models.csv', 'w', newline="") as csv_file:
    writer = csv.writer(csv_file)
    for model in models:
        writer.writerow(model.values())

results = p_umap(run_simulation, models)
print("time for writing the results")
with open('out.csv', "a") as file:
    for result in results:
        file.write('{:.2f},{:d},{:d},{:},{:},{:d}, {:d}\n'.format(
            result["density"], int(result["incubation_time"]),
            int(result["iteration"]), result["seed"], result["winner"],
            result["steps"], int(result["grouping"])
        ))
