import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

def density_index(i):
    return int(i * 10 - 0.5)

def incubation_index(i):
    return int(i * (1 / 3))

vals = []

for _ in range(10):
    vals.append([0] * 5)

with open('out.csv', 'r') as file:
    reader = csv.reader(file, delimiter=',')

    for result in reader:
        if result[4] == 'human':
            di = density_index(float(result[0]))
            ii = incubation_index(int(result[1]))

            vals[di][ii] += 1

plt.imshow(vals, vmin=10, vmax=25, cmap='BuGn', interpolation='spline16', origin='lower', aspect='0.5')
cbar = plt.colorbar(ticks=[10, 25])

cbar.ax.set_yticklabels(['40%', '100%'])

# cbar.ax.set_ylabel('Out of 25 simulations', rotation=90)

ax = plt.axes()

ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, pos: (x + 1) * 3))
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, pos: "{:d}".format(int(100 * (0.1 * y + 0.05)))))

plt.xlabel("Incubation time")
plt.ylabel("Population density (in %)")
plt.title("Human survival rate")

# ax.xaxis.set_major_formatter(plt.NullFormatter())

plt.tight_layout()
# plt.show()

plt.savefig('heatmap.pdf')
