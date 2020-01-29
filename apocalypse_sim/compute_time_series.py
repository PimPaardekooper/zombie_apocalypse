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
import json

print("1")
def read_last_line(filename):
    return subprocess.check_output(['tail', '-1', filename])[0:-1].decode('utf-8')

def delete_last_line(filename):
    subprocess.check_output(['sed', '-i', '$d', filename])



# Default parameters for iterators
density_stepsize = 0.1
inc_time_stepsize = 6
simulation_stepsize = 1

density_start = 0.05
inc_time_start = 12
simulation_start = 0

# Ends (exclusive)
density_end = 0.35
inc_time_end = 13
simulation_end = 50

# last_experiment = read_last_line(filename)

os.environ["mode"] = "3"

def get_model_params():
    return {
        "width": 30,
        "height": 30,
        "density": None,
        "infected_chance": 0.05,
        "incubation_time": None,
        "map_id": 0,
        "human_kill_agent_chance": 0.35
    }

densities = np.arange(density_start, density_end, density_stepsize)
inc_times = np.arange(inc_time_start, inc_time_end, inc_time_stepsize)
simulations = np.arange(simulation_start, simulation_end, simulation_stepsize)

first = True

def run_simulation(params):
    model = Apocalypse(**params)
    series = []
    it = 0
    while True:
        it += 1
        model.step()
        series.append((model.susceptible, model.infected, model.carrier))
        if (model.infected == 0 and model.carrier == 0) or (model.susceptible == 0):
            return {"data": series, "density": str(params["density"]), "incubation_time": str(params["incubation_time"])}
        # Zombies win
        if it > 100:
            return {"data": series, "density": str(params["density"]), "incubation_time": str(params["incubation_time"])}

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
with open('series.json', "w") as file:
    file.write(json.dumps(results))
