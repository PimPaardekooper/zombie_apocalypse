import sys
sys.path.append("..")
from model import Apocalypse
import os
import numpy as np
import random
import csv
from p_tqdm import p_umap

os.environ["mode"] = "3"


def get_model_params():
    """Get the parameters needed for running the model."""
    return {
        "width": 50,
        "height": 50,
        "density": None,
        "infected_chance": 0.05,
        "map_id": 0,
        "grouping": None,
        "human_kill_agent_chance": 0.35
    }


output_file = "group_output2.csv"

# TODO::Check if exist add number

columns = [
    "density", "group", "iteration",
    "seed", "winner", "steps"
]

density_stepsize = 0.1
density_start = 0.05
density_end = 0.5
densities = np.arange(density_start, density_end, density_stepsize)

simulation_start = 0
simulation_end = 10
simulation_stepsize = 1
simulations = np.arange(simulation_start, simulation_end, simulation_stepsize)


def run_simulation(params):
    """Run the simulation with the given parameters."""
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
    for group in [True, False]:
        for iteration in simulations:
            # Fix simulations iterator after updating
            # the unfinished experiment
            model = get_model_params()
            model["density"] = density
            model["grouping"] = group
            model["seed"] = str(random.randrange(sys.maxsize))
            model["iteration"] = iteration
            models.append(model)

with open('models.csv', 'w', newline="") as csv_file:
    writer = csv.writer(csv_file)
    for model in models:
        writer.writerow(model.values())

results = p_umap(run_simulation, models)
print("time for writing the results")
with open(output_file, "a") as file:
    for result in results:
        file.write('{:.2f},{:d},{:d},{:},{:},{:d}\n'.format(
            result["density"], int(result["grouping"]),
            int(result["iteration"]), result["seed"], result["winner"],
            result["steps"]
        ))
