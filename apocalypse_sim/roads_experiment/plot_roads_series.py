"""Plot incubation time against percentage infected.

Plot the result of the road experiment.
"""
import json
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt


def read_series_compute_percentage_infected():
    """Read and return data with percentage infected added."""
    d = {}

    with open('series_road.json') as json_file:
        data = json.load(json_file)
        for item in tqdm(data):
            series = item['data']
            density = item['density']
            incubation = item['incubation_time']

            for i, x in enumerate(series):
                if x[0] == 0:
                    p = 0
                else:
                    p = ((x[1] + x[2]) / (x[0] + x[1] + x[2])) * 100

                if incubation in d:
                    d[incubation].append([i, p, float(density),
                                          int(incubation)])
                else:
                    d[incubation] = []
                    d[incubation].append([i, p, float(density),
                                          int(incubation)])

    return d


def plot_series(d):
    """Plot percentage infected against the incubation time."""
    f, axes = plt.subplots(1, 1, figsize=(7, 7), sharex=True)

    counter = 0
    for i, inc in enumerate(d):
        serie = pd.DataFrame(d[inc], columns=['step',
                                              'percentage_infected',
                                              'density',
                                              'incubation_time'])

        plot = sns.lineplot(x="step",
                            y="percentage_infected",
                            hue="incubation_time",
                            markers=True,
                            dashes=False,
                            data=serie,
                            legend="full",
                            ax=axes)
        counter += 1

    plot.title("Percentage infected by different incubation times.")
    plot.legend(fontsize='10', loc="upper left")
    plot.get_figure().savefig("outputs/output3.pdf")


if __name__ == "__main__":
    d = read_series_compute_percentage_infected()
    plot_series(d)