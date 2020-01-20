"""map_layouts.py

Hold the layout and situations, here you should make situations.
"""
from .map_object import Place, Road
import pygeoj
import numpy as np
import pandas as pd
from mode import is_verification
# TODO: delete
from shapely.geometry import Point

class Map:

    def __init__(self, map_id, model):
        self.model = model

        maps = [self.initial_map, self.second_map, self.third_map, self.fourth_map, self.fifth_map,
                self.sixth_map, self.situation_map, self.nethelands_map]

        if is_verification():
            maps = [
                self.convert_test, self.range_test, self.runaway_test,
                self.group_test, self.third_map, self.fourth_map,
                self.fifth_map, self.sixth_map, self.situation_map
            ]

        self.places, self.roads, self.agents = maps[map_id]()

    def nethelands_map(self):

        cities = []


        poly_data = pygeoj.load(filepath="netherlands_data/provincie_2020.geojson")
        df = pd.read_csv("netherlands_data/provinces_densities.csv")

        min_dens = df["density_of_total"].min()
        max_dens = df["density_of_total"].max()

        for feature in poly_data:
            color = "".join(["{0:02X}".format(x) for x in
                            np.random.choice(range(256), size=3)])
            color = "#" + color
            statnaam = feature.properties["statnaam"]

            if feature.geometry.type == "Polygon":
                for polygon in feature.geometry.coordinates:
                    vert = self.stretch_to_grid(polygon, poly_data)
                    dens = df[df["statnaam"] == statnaam]["density_of_total"].values[0]
                    dens = self.stretch_density(dens, min_dens, max_dens) * self.model.density
                    province = Place(vert, dens, name=statnaam, color=color)

                    cities.append(province)

            elif feature.geometry.type == "MultiPolygon":
                for m_poly in feature.geometry.coordinates:
                    for polygon in m_poly:
                        vert = self.stretch_to_grid(polygon, poly_data)
                        province = Place(vert, 0, name=statnaam, color=color)
                        dens = df[df["statnaam"] == statnaam]["density_of_total"].values[0]
                        dens = self.stretch_density(dens, min_dens, max_dens) * self.model.density
                        province = Place(vert, dens, name=statnaam, color=color)

                        cities.append(province)

        road1 = Place([[88,156], [87,157], [104, 168], [104,166]], 0)
        road2 = Place([[101,139], [99,138], [110, 129], [111,129]], 0)
        road3 = Place([[25,42], [26,42], [26, 45], [24,45]], 0)
        road4 = Place([[28,74], [26,74], [25, 72], [26,71]], 0)

        return cities, [road1, road2, road3, road4], []

    def stretch_density(self, dens, min_dens, max_dens):
        """Stretch dens between 0.1 and 1."""
        return (dens - min_dens)/(max_dens - min_dens) * 0.9 + 0.1

    def stretch_to_grid(self, polygon, data):
        min_x, min_y, max_x, max_y = data.bbox

        xs = [x[0] for x in polygon]
        ys = [x[1] for x in polygon]

        xs = [(x - min_x)/(max_x - min_x) * (200) for x in xs]
        ys = [(y - min_y)/(max_y - min_y) * (200) for y in ys]
        vert = list(zip(xs, ys))

        return vert


    def initial_map(self):
        """Square map no walls."""
        city = Place([[0, 0],
                      [0, self.model.grid.height],
                      [self.model.grid.width,
                       self.model.grid.height],
                      [self.model.grid.width, 0],
                      [0, 0]],
                     self.model.density)

        return [city], [], []

    def second_map(self):
        """
        Map that has a city and village and a road between. Every point that is
        not inside it you can't walk.
        """
        city = Place([[50, 75],
                      [75, 75],
                      [75, 50],
                      [50, 50],
                      [50, 75]],
                     0.3)

        village = Place([[5, 5], [10, 5], [10, 10], [5, 10], [5, 5]], 0.1)

        road = Road([[8, 10], [10, 8], [52, 50], [50, 52], [8, 10]], (1, 1), 2)

        return [city, village], [road], []

    def third_map(self):
        """
        Map that has no roads.
        """
        city = Place([[50, 75],
                      [75, 75],
                      [75, 50],
                      [50, 50],
                      [50, 75]],
                     0.3)

        village = Place([[49, 70], [49, 55], [
                        30, 55], [30, 70], [49, 70]],
                        0.1)

        return [city, village], [], []

    def fourth_map(self):
        city1 = Place([[35, 37], [37, 35], [35, 65], [65, 65],
                       [65, 35], [35, 37]], self.model.density)

        city2 = Place([[15, 15], [15, 25], [23, 25], [25, 23],
                       [25, 15], [15, 15]], self.model.density)
        city3 = Place([[75, 75], [75, 85], [85, 85], [
                      85, 75], [75, 75]], self.model.density)
        city4 = Place([[15, 75], [15, 85], [25, 85], [
                      25, 75], [15, 75]], self.model.density)
        city5 = Place([[75, 15], [85, 15], [85, 25], [
                      75, 25], [75, 15]], self.model.density)

        road = Road([[23, 25], [25, 23], [37, 35],
                     [35, 37], [23, 25]], (1, 1), 2)

        road2 = Road([[77, 75], [75, 77], [60, 62],
                      [62, 60], [77, 75]], (1, 1), 2)

        road3 = Road([[77, 25], [75, 22], [62, 35],
                      [65, 36], [77, 25]], (1, 1), 2)

        road4 = Road([[25, 77], [22, 75], [35, 61],
                      [37, 65], [25, 77]], (1, 1), 2)

        return [city1, city2, city3, city4, city5], [road, road2, road3, road4], []

    def fifth_map(self):
        city1 = Place([[10, 90], [10, 70], [25, 70], [30, 75],
                       [30, 90], [10, 90]], self.model.density)
        city2 = Place([[10, 10], [30, 10], [30, 25], [25, 30],
                       [10, 30], [10, 10]], self.model.density)
        city3 = Place([[70, 10], [90, 10], [90, 30], [75, 30],
                       [70, 25], [70, 10]], self.model.density)
        city4 = Place([[90, 70], [90, 90], [70, 90], [70, 75],
                       [75, 70], [90, 70]], self.model.density)
        city5 = Place([[40, 55], [40, 45], [45, 40], [55, 40], [60, 45], [60, 55],
                       [55, 60], [45, 60], [40, 55]], self.model.density)

        city6 = Place([[0, 40], [0, 60], [20, 60], [20, 40]],
                      self.model.density)
        city7 = Place([[40, 0], [60, 0], [60, 20], [40, 20]],
                      self.model.density)
        city8 = Place([[80, 40], [80, 60], [100, 60],
                       [100, 40]], self.model.density)
        city9 = Place([[40, 80], [60, 80], [60, 100],
                       [40, 100]], self.model.density)

        road1 = Road([[25, 30], [30, 25], [45, 40], [40, 45]], (1, 1), 2)
        road2 = Road([[55, 40], [60, 45], [75, 30], [70, 25]], (1, 1), 2)
        road3 = Road([[60, 55], [75, 70], [70, 75], [55, 60]], (1, 1), 2)
        road4 = Road([[30, 75], [25, 70], [40, 55], [45, 60]], (1, 1), 2)

        # Horizontal
        road5 = Road([[45, 40], [55, 40], [55, 20], [45, 20]], (0, 1), 2)
        road6 = Road([[45, 60], [55, 60], [55, 80], [45, 80]], (0, 1), 2)

        # Vertical
        road7 = Road([[40, 45], [40, 55], [20, 55], [20, 45]], (1, 0), 2)
        road8 = Road([[60, 45], [60, 55], [80, 55], [80, 45]], (1, 0), 2)

        return [city1, city2, city3, city4, city5, city6, city7, city8, city9], \
            [road1, road2, road3, road4, road5, road6, road7, road8], []

    def sixth_map(self):
        city1 = Place([[40, 55], [40, 45], [45, 40], [55, 40], [60, 45], [60, 55],
                       [55, 60], [45, 60], [40, 55]], self.model.density)

        city2 = Place([[0, 0], [0, 20], [15, 20], [20, 15],
                       [20, 0], [0, 0]], self.model.density)
        city3 = Place([[80, 0], [100, 0], [100, 20], [85, 20],
                       [80, 15], [80, 0]], self.model.density)
        city4 = Place([[100, 80], [100, 100], [80, 100], [80, 85], [
                      85, 80], [100, 80]], self.model.density)
        city5 = Place([[20, 100], [0, 100], [0, 80], [15, 80],
                       [20, 85], [20, 100]], self.model.density)

        city6 = Place([[0, 40], [0, 60], [20, 60], [20, 40]],
                      self.model.density)
        city7 = Place([[40, 0], [60, 0], [60, 20], [40, 20]],
                      self.model.density)
        city8 = Place([[80, 40], [80, 60], [100, 60],
                       [100, 40]], self.model.density)
        city9 = Place([[40, 80], [60, 80], [60, 100],
                       [40, 100]], self.model.density)

        road1 = Road([[15, 20], [20, 15], [45, 40], [40, 45]], (1, 1), 2)
        road2 = Road([[55, 40], [60, 45], [85, 20], [80, 15]], (1, 1), 2)
        road3 = Road([[60, 55], [85, 80], [80, 85], [55, 60]], (1, 1), 2)
        road4 = Road([[20, 85], [15, 80], [40, 55], [45, 60]], (1, 1), 2)

        # Horizontal
        road5 = Road([[45, 40], [55, 40], [55, 20], [45, 20]], (0, 1), 2)
        road6 = Road([[45, 60], [55, 60], [55, 80], [45, 80]], (0, 1), 2)

        # Vertical
        road7 = Road([[40, 45], [40, 55], [20, 55], [20, 45]], (1, 0), 2)
        road8 = Road([[60, 45], [60, 55], [80, 55], [80, 45]], (1, 0), 2)

        road9 = Road([[5, 20], [15, 20], [15, 40], [5, 40]], (0, 1), 2)
        road10 = Road([[5, 60], [15, 60], [15, 80], [5, 80]], (0, 1), 2)

        road11 = Road([[85, 60], [95, 60], [95, 80], [85, 80]], (0, 1), 2)
        road12 = Road([[85, 20], [95, 20], [95, 40], [85, 40]], (0, 1), 2)

        road13 = Road([[20, 5], [20, 15], [40, 15], [40, 5]], (1, 0), 2)
        road14 = Road([[60, 5], [60, 15], [80, 15], [80, 5]], (1, 0), 2)

        road15 = Road([[60, 85], [60, 95], [80, 95], [80, 85]], (1, 0), 2)
        road16 = Road([[20, 85], [20, 95], [40, 95], [40, 85]], (1, 0), 2)

        return [city1, city2, city3, city4, city5, city6, city7, city8, city9], \
            [road1, road2, road3, road4, road5, road6, road7, road8, road9,
             road10, road11, road12, road13, road14, road15, road16], []

    def situation_map(self):
        """Square map no walls."""
        city = Place([[0, 0],
                      [0, self.model.grid.height],
                      [self.model.grid.width,
                       self.model.grid.height],
                      [self.model.grid.width, 0],
                      [0, 0]],
                     0)

        humans = Agents("human", [(0, 1), (1, 0)])

        return [city], [], [humans]

    ### TEST MAPS ###
    def convert_test(self):
        humans = Agents("human", [(0, 1)])
        zombies = Agents("zombie", [(0, 2)])
        city = Place([[0, 0],
                [0, self.model.grid.height],
                [self.model.grid.width,
                self.model.grid.height],
                [self.model.grid.width, 0],
                [0, 0]],
                0)

        return [city], [], [humans, zombies]


    def range_test(self):
        """Square map no walls."""
        city = Place([[0, 0],
                      [0, self.model.grid.height],
                      [self.model.grid.width,
                       self.model.grid.height],
                      [self.model.grid.width, 0],
                      [0, 0]],
                     0)

        humans = Agents("human", [(0, 0)])
        zombies = Agents("zombie", [(0, 7)])

        return [city], [], [humans, zombies]

    def runaway_test(self):
        """Square map no walls."""
        city = Place([[0, 0],
                      [0, self.model.grid.height],
                      [self.model.grid.width,
                       self.model.grid.height],
                      [self.model.grid.width, 0],
                      [0, 0]],
                     0)

        humans = Agents("human", [(0, 5)])
        zombies = Agents("zombie", [(0, 9)])

        return [city], [], [humans, zombies]


    def group_test(self):
        """Square map no walls."""
        city = Place([[0, 0],
                      [0, self.model.grid.height],
                      [self.model.grid.width,
                       self.model.grid.height],
                      [self.model.grid.width, 0],
                      [0, 0]],
                     0)

        humans = Agents("human", [(0, 0), (4, 0), (0, 4), (3, 3)])

        return [city], [], [humans]


class Agents:
    def __init__(self, agent_type, positions, attr={}):
        self.agent_type = agent_type
        self.positions = positions
        self.attr = attr
