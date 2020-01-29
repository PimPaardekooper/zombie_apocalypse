import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd

vals = {}

with open('data/density_and_incubation_nogrouping.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')

    for result in reader:
        density = result[0]
        incubation = result[1]
        winner = result[4]

        if density not in vals:
            vals[density] = {}

        if incubation not in vals[density]:
            vals[density][incubation] = 0

        if winner == 'human':
            vals[density][incubation] += 1

result = []

for i, k in enumerate(sorted(vals.keys(), key=lambda x: float(x))):
    f = vals[k].keys()

    result.append([0] * len(f))

    for j, m in enumerate(sorted(f, key=lambda x: int(x))):
        result[i][j] = vals[k][m]

plt.imshow(result, vmin=0, vmax=25, cmap='BuGn', interpolation='spline16', origin='lower')

m = np.array(result)
win_min = m.min()
win_max = m.max()

cbar = plt.colorbar(ticks=[0, 25])

cbar.ax.set_yticklabels(["{:d}%".format(int(100 * (0 / 25))), "{:d}%".format(int(100 * (25 / 25)))])

cbar.ax.set_ylabel('Out of 25 simulations', rotation=90)

ax = plt.axes()

ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: x * 3))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: "{:d}".format(int(100 * (0.1 * y + 0.05)))))

plt.xlabel("Incubation time")
plt.ylabel("Population density (in %)")
plt.title("Human survival rate")

plt.tight_layout()
# plt.show()

plt.savefig('results/density_and_incubation_nogrouping.pdf')
