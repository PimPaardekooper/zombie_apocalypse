from model import Apocalypse
import numpy as np
import random
import sys
import os
import subprocess
import time

filename = "output-pim.csv"

def read_last_line(filename):
    return subprocess.check_output(['tail', '-1', filename])[0:-1].decode('utf-8')

def delete_last_line(filename):
    subprocess.check_output(['sed', '-i', '$d', filename])

def get_model_params():
    return {
        "width": 50,
        "height": 50,
        "density": None,
        "infected_chance": 0.05,
        "incubation_time": None,
        "map_id": 0,
        "human_kill_agent_chance": 0.35
    }

# Default parameters for iterators
density_stepsize = 0.10
inc_time_stepsize = 2
simulation_stepsize = 1

density_start = 0.35
inc_time_start = 0
simulation_start = 0

# Ends (exclusive)
density_end = 0.55
inc_time_end = 22
simulation_end = 50

last_experiment = read_last_line(filename)

os.environ["mode"] = "3"

# At least one experiment was done already
if len(last_experiment):
    # Delete the last unfinished experiment, so that
    # we can continue from there.
    delete_last_line(filename)

    last_experiment = last_experiment.split(",")

    # Update iterator's start parameters
    density_start = float(last_experiment[0])
    inc_time_start = int(last_experiment[1])
    simulation_start = int(last_experiment[2])

densities = np.arange(density_start, density_end, density_stepsize)
inc_times = np.arange(inc_time_start, inc_time_end, inc_time_stepsize)
simulations = np.arange(simulation_start, simulation_end, simulation_stepsize)

first = True

def run_simulation(params):
    model = Apocalypse(**params)

    while True:
        model.step()

        # Zombies win
        if model.susceptible == 0:
            return params['seed'], 'zombies', model.schedule.steps

        # Humans win
        elif model.infected == 0 and model.carrier == 0:
            return params['seed'], 'humans', model.schedule.steps

with open(filename, "a") as file:
    model_params = get_model_params()

    # Loop through iterators
    for density in densities:
        model_params["density"] = density

        for incubation_time in inc_times:
            model_params["incubation_time"] = incubation_time

            for iteration in simulations.copy():

                # Fix simulations iterator after updating
                # the unfinished experiment
                if first:
                    simulations = np.arange(
                        0, simulation_end, simulation_stepsize
                    )

                    first = False

                model_params["seed"] = str(random.randrange(sys.maxsize))

                seed, winner, steps = run_simulation(model_params)

                # Write experiment to file
                file.write('{:.2f},{:d},{:d},{:},{:},{:d}\n'.format(
                    density, int(incubation_time), int(iteration),
                    seed, winner, steps
                ))