from model import Apocalypse
import numpy as np
import random
import sys
import os
import csv
import subprocess
from io import StringIO

filename = "output.csv"
lastline = subprocess.check_output(['tail', '-1', filename]).decode('utf-8')[0:-1]

columns = [
    "density", "incubation_time", "iteration",
    "seed", "winner", "steps"
]

# Read last experiment
with StringIO(lastline) as fa:
    last_experiment = csv.reader(fa, delimiter=',', quotechar='"')

    # Load last experiment into variable
    for x in last_experiment:
        last_experiment = x

        break


def delete_last_line(file):
    file.seek(0, os.SEEK_END)

    pos = file.tell() - 1

    while pos > 0 and file.read(1) != "\n":
        pos -= 1
        file.seek(pos, os.SEEK_SET)

    if pos >= 0:
        file.seek(pos, os.SEEK_SET)
        file.truncate()


# Default parameters for iterators
density_stepsize = 0.10
inc_time_stepsize = 2
simulation_stepsize = 1

density_start = 0.05
inc_time_start = 0
simulation_start = 0

# Ends (exclusive)
density_end = 0.25
inc_time_end = 3
simulation_end = 10

ie = False

with open(filename, "r+") as fb:

    # At least one experiment was done already
    if isinstance(last_experiment, list):
        # Delete the last unfinished experiment, so that
        # we can continue from there.
        delete_last_line(fb)

        ie = True

        # Update iterator's start parameters
        density_start = float(last_experiment[columns.index("density")])
        inc_time_start = int(last_experiment[columns.index("incubation_time")])
        simulation_start = int(last_experiment[columns.index("iteration")])

densities = np.arange(density_start, density_end, density_stepsize)
inc_times = np.arange(inc_time_start, inc_time_end, inc_time_stepsize)
simulations = np.arange(simulation_start, simulation_end, simulation_stepsize)

first = True

with open(filename, "a") as fc:

    # Make sure the output file ends with a new line,
    # so our data won't get messed up
    if ie:
        fc.write("\n")

    # Loop through iterators
    for a in densities:
        for b in inc_times:
            for c in simulations.copy():

                # Fix simulations iterator after updating
                # the unfinished experiment
                if first:
                    simulations = np.arange(
                        0, simulation_end, simulation_stepsize
                    )

                    first = False

                # Write experiment to file
                fc.write('"{}","{}","{}"\n'.format(a, b, c))
