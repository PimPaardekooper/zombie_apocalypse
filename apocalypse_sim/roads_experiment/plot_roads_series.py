"""Plot incubation time against percentage infected.

Plot the result of the road experiment.
"""
import json
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt


def read_series_compute_percentage_infected(data_file):
    """Read and return data with percentage infected added."""
    d = {}

    with open(data_file) as json_file:
        data = json.load(json_file)
        for item in tqdm(data):
            series = item['data']
            density = item['density']
            incubation = item['incubation_time']

            for i, x in enumerate(series):
                if x[0] == 0:
                    p = 0
                else:
                    p = ((x[1] + x[2] + x[3]) / (x[0] + x[1] + x[2] + x[3])) \
                        * 100

                if incubation in d:
                    d[incubation].append([i, p, float(density),
                                          int(incubation)])
                else:
                    d[incubation] = []
                    d[incubation].append([i, p, float(density),
                                          int(incubation)])

    return d


def plot_series(d, output_file):
    """Plot percentage infected against the incubation time."""
    _, axes = plt.subplots(1, 1, figsize=(7, 7), sharex=True)
    palette = sns.color_palette('coolwarm', n_colors=len(d))
    series = []

    for _, inc in enumerate(d):
        serie = pd.DataFrame(d[inc], columns=['step',
                                              'percentage_infected',
                                              'density',
                                              'incubation_time'])
        series.append(serie)

    serie = pd.concat(series)
    plot = sns.lineplot(x="step",
                        y="percentage_infected",
                        hue="incubation_time",
                        markers=True,
                        dashes=False,
                        data=serie,
                        legend="full",
                        ax=axes,
                        palette=palette)

    # plot.title("Percentage infected by different incubation times.")
    plot.legend(fontsize='10', loc="upper left")
    plot.get_figure().savefig(output_file)


if __name__ == "__main__":
    data_file = "data/road_series.json"
    output_file = "results/road_output.pdf"
    d = read_series_compute_percentage_infected(data_file)
    plot_series(d, output_file)
