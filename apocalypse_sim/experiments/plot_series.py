""" Plot a time series comparing 5% vs 25% density on a 12 step incubation time.
"""
import json
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
import seaborn as sns
d = []
with open('series.json') as json_file:
    data = json.load(json_file)
    for item in tqdm(data):
        series = item['data']
        density = item['density']
        incubation = item['incubation_time']
        if (float(density) == 0.25 or float(density) == 0.05) and (int(incubation) == 12):
            # print(incubation)
            for i, x in enumerate(series):
                p = (x[1] + x[2]) / ( x[0] + x[1] + x[2] ) * 100
                d.append([i, p, float(density), int(incubation)])
serie = pd.DataFrame(d, columns=['step', 'percentage infected', 'density', 'incubation time'])
plot = sns.lineplot(x="step", y="percentage infected",
                  hue="density",
                  markers=True, dashes=False, data=serie,  legend="full")

plot.get_figure().savefig("results/series.pdf")