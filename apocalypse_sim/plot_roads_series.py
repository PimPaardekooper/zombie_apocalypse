import json
from collections import defaultdict
import pandas as pd
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt

d = {}
with open('series2.json') as json_file:
    data = json.load(json_file)
    for item in tqdm(data):
        series = item['data']
        print(series)
        density = item['density']
        incubation = item['incubation_time']


        # print(incubation)
        for i, x in enumerate(series):
            if x[0] == 0:
                p = 0
            else:
                p = ((x[1] + x[2]) / (x[0] + x[1] + x[2])) * 100

            if density in d:
                if incubation in d[density]:
                    d[density][incubation].append([i, p, float(density), int(incubation)])
                else:
                    d[density][incubation] = []
                    d[density][incubation].append([i, p, float(density), int(incubation)])
            else:

                d[density] = {}
                d[density][incubation] = []
                d[density][incubation].append([i, p, float(density), int(incubation)])


f, axes = plt.subplots(3, 1 , figsize=(7, 7), sharex=True)

plt.legend(fontsize='10')

counter = 0
for i, dens in enumerate(d):
    series = []
    for j, inc in enumerate(d[dens]):
        series.append(pd.DataFrame(d[dens][inc],
                    columns=['step', 'percentage_infected', 'density',
                            'incubation_time']))

    serie = pd.concat(series)

    if i == 0 or i == 4:
        print(i)
        continue
    print(i)
# serie = serie.loc[serie['density'] = str(0.15)]
# print(serie)
# serie = pd.read_csv('series.csv')
    # print(dens, inc)
    # print(serie)
    # print("\n\n")
    print(i, dens)
    axes[counter].set_title("density {}".format(dens))
    plot = sns.lineplot(x="step", y="percentage_infected",
                    hue="incubation_time",
                    markers=True, dashes=False, data=serie, legend="full",
                    ax=axes[counter])
    counter += 1

plot.get_figure().savefig("outputs/output3.pdf")
