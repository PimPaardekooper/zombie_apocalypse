import requests
from bs4 import BeautifulSoup
import pandas as pd

def to_english_notation(string):
    return string.decode('utf-8').replace(".", "").replace(",", ".")

url = requests.get("http://nl.wikipedia.org/wiki/Provincies_van_Nederland").text

soup = BeautifulSoup(url, "lxml")

my_table = soup.find('table', {'class': 'wikitable sortable'})

#headers = my_table.findAll('th')

#for x in headers:
#    print(x.find('a'))

#print(my_table)
rows = my_table.findAll('tr')

df = pd.DataFrame(columns=['statnaam', 'population', 'surface', 'population_per_km'])


for i, x in enumerate(rows[1:]):
    tds = x.findAll('td')
    province = tds[1].find('a').renderContents()
    bevolking = tds[2].renderContents()
    oppervlakte = tds[4].renderContents()
    bevolkingsdichtheid = tds[5].renderContents()

    df.loc[i] = [str(province.decode('utf-8')), float(to_english_notation(bevolking)), float(to_english_notation(oppervlakte)),
          int(to_english_notation(bevolkingsdichtheid))]

df["density_of_total"] = df["population_per_km"].apply(lambda x: float(x)/float(df["population_per_km"].sum()))

df.to_csv("provinces_densities.csv")
