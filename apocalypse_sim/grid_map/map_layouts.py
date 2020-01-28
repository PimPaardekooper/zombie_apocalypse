"""map_layouts.py.

Hold the layout and situations, here you should make situations.
"""
from .map_object import Place, Road
import pygeoj
import numpy as np
import pandas as pd
import os


class Map:
    """Map object.

    Hold the maps for each modes and contains all map object polygons and
    attributes
    """

    def __init__(self, map_id, model):
        """Initialise Map.

        Get maps for the mode and choices one out of it.
        map_id: id of map in list.
        model: holds the Apocalypse model.
        """
        self.model = model

        if os.environ["mode"] == "1":
            maps = [
                self.convert_test, self.range_test, self.runaway_test,
                self.group_test
            ]
        elif os.environ["mode"] == "2":
            maps = [self.nethelands_map]
        elif os.environ["mode"] == "3":
            maps = [self.simple_incubation]
        elif os.environ["mode"] == "4":
            maps = [self.doorway_map]
        elif os.environ["mode"] == "5":
            maps = [self.road_map]
        else:
            maps = [
                self.initial_map, self.second_map, self.third_map,
                self.fourth_map, self.fifth_map, self.sixth_map,
                self.situation_map
            ]

        self.places, self.roads, self.agents = maps[map_id]()

    def doorway_map(self):
        """One city with a doorway at the top."""
        city = Place([[0, 0],
                      [0, self.model.height*0.75],
                      [self.model.width, self.model.height*0.75],
                      [self.model.width, 0]],
                     0)

        city2 = Place([[self.model.width*0.25, self.model.height*0.25],
                       [self.model.width*0.5, self.model.height*0.5],
                       [self.model.width*0.75, self.model.height*0.25]],
                      self.model.density)

        offset = ((self.model.width-self.model.door_width)/self.model.width)/2

        road = Road([[self.model.width*offset, self.model.height*0.75],
                     [self.model.width*(1-offset), self.model.height*0.75],
                     [self.model.width*(1-offset), self.model.height],
                     [self.model.width*offset, self.model.height]], (0, 0), 0)

        self.model.door = [
            (int(self.model.width*offset), int(self.model.height)-1),
            (int(self.model.width*(1-offset)), int(self.model.height)-1)
        ]

        zombies = Agents(
            "zombie",
            [(int(self.model.width*0.5), int(self.model.height*0.20))]
        )

        return [city, city2], [road], [zombies]

    def nethelands_map(self):
        """Map of holland.

        Gets the polygons for each province out of a geojson file and the
        densities of each province out of csv file. They are coupled with the
        'statnaam'.

        Polygons are in longitude latitude, this is converted to the range
        200, 200. It therefore needs to be called for a grid of 200 by 200.

        The densities are person per km and needs to fit on the grid, therefore
        we stretch it between 0.1 and 1. So relative the densities represent
        real data.
        """
        cities = []

        poly_data = pygeoj.load(
            filepath="grid_map/data/provincie_2020.geojson")
        df = pd.read_csv("grid_map/data/provinces_densities.csv")

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
                    dens = df[df["statnaam"] ==
                              statnaam]["density_of_total"].values[0]
                    dens = self.stretch_density(
                        dens, min_dens, max_dens) * self.model.density
                    province = Place(vert, dens, name=statnaam, color=color)

                    cities.append(province)

            elif feature.geometry.type == "MultiPolygon":
                for m_poly in feature.geometry.coordinates:
                    for polygon in m_poly:
                        vert = self.stretch_to_grid(polygon, poly_data)
                        dens = df[df["statnaam"] ==
                                  statnaam]["density_of_total"].values[0]
                        dens = self.stretch_density(
                            dens, min_dens, max_dens) * self.model.density
                        province = Place(
                            vert, dens, name=statnaam, color=color)

                        if province.poly.area > 10:
                            cities.append(province)

        road1 = Place([[88, 156], [87, 157], [104, 168], [104, 166]], 0)
        road2 = Place([[101, 139], [99, 138], [110, 129], [111, 129]], 0)
        road3 = Place([[25, 42], [26, 42], [26, 45], [24, 45]], 0)
        road4 = Place([[28, 74], [26, 74], [25, 72], [26, 71]], 0)

        road5 = Place([[71, 157], [72, 157], [72, 160], [71, 160]], 0)
        road6 = Place([[79, 176], [80, 175], [79, 173], [78, 174]], 0)

        road7 = Place([[88, 183], [90, 182], [94, 187], [94, 188]], 0)

        road8 = Place([[112, 192], [113, 191], [117, 192], [117, 193]], 0)

        road9 = Place([[133, 194], [134, 193], [144, 195], [144, 196]], 0)

        roades = [road1, road2, road3, road4, road5, road6, road7, road8,
                  road9]

        return cities, roades, []

    def stretch_density(self, dens, min_dens, max_dens):
        """Stretch dens between 0.1 and 1."""
        return (dens - min_dens)/(max_dens - min_dens) * 0.9 + 0.1

    def stretch_to_grid(self, polygon, data):
        """Fit polygon to grid.

        Stretch the given polygon data to a grid of 200 by 200. Given all
        polygons.
        """
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
        """Second map.

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
        """Map that has no roads."""
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
        """Five cities connected through middle city."""
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

        cities = [city1, city2, city3, city4, city5]
        roads = [road, road2, road3, road4]

        return cities, roads, []

    def fifth_map(self):
        """Five cities connected middle city and corners are connected."""
        city1 = Place([[10, 90], [10, 70], [25, 70], [30, 75],
                       [30, 90], [10, 90]], self.model.density)
        city2 = Place([[10, 10], [30, 10], [30, 25], [25, 30],
                       [10, 30], [10, 10]], self.model.density)
        city3 = Place([[70, 10], [90, 10], [90, 30], [75, 30],
                       [70, 25], [70, 10]], self.model.density)
        city4 = Place([[90, 70], [90, 90], [70, 90], [70, 75],
                       [75, 70], [90, 70]], self.model.density)
        city5 = Place([[40, 55], [40, 45], [45, 40], [55, 40], [60, 45],
                       [60, 55], [55, 60], [45, 60], [40, 55]],
                      self.model.density)

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

        cities = [city1, city2, city3, city4, city5, city6, city7, city8,
                  city9]

        roads = [road1, road2, road3, road4, road5, road6, road7, road8]

        return cities, roads, []

    def sixth_map(self):
        """Nine cities 3 in a row, all neighbor cities are connected."""
        city1 = Place([[40, 55], [40, 45], [45, 40], [55, 40], [60, 45],
                       [60, 55], [55, 60], [45, 60], [40, 55]],
                      self.model.density)

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

        cities = [city1, city2, city3, city4, city5, city6, city7, city8,
                  city9]

        roads = [road1, road2, road3, road4, road5, road6, road7, road8, road9,
                 road10, road11, road12, road13, road14, road15, road16]

        return cities, roads, []

    def road_map(self):
        """$ cities vertical and horizontal connected."""
        city1 = Place([[0, 0], [0, 9], [9, 9], [0, 9]],
                      self.model.density)

        city2 = Place([[20, 9], [20, 0], [29, 0], [29, 9]],
                      self.model.density)

        city3 = Place([[20, 20], [29, 20], [29, 29], [20, 29]],
                      self.model.density)

        city4 = Place([[9, 20], [0, 20], [0, 29], [9, 29]],
                      self.model.density)

        road1 = Road([[2, 19], [2, 10], [7, 10], [7, 19]], (0, 1), 2)
        road2 = Road([[10, 7], [10, 2], [19, 2], [19, 7]], (1, 0), 2)
        road3 = Road([[22, 10], [27, 10], [27, 19], [22, 19]], (0, 1), 2)
        road4 = Road([[10, 27], [19, 27], [19, 22], [10, 22]], (1, 0), 2)

        return [city1, city2, city3, city4], [road1, road2, road3, road4], []

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

    def convert_test(self):
        """Test if the transition from zombie to human works."""
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

        humans = Agents("human", [(9, 0), (9, 1), (8, 1), (8, 0)])
        zombies = Agents("zombie", [(0, 9), (0, 8)])

        return [city], [], [humans, zombies]

    def simple_incubation(self):
        """Square map no walls."""
        city = Place([[0, 0],
                      [0, self.model.grid.height],
                      [self.model.grid.width,
                       self.model.grid.height],
                      [self.model.grid.width, 0],
                      [0, 0]],
                     self.model.density)

        return [city], [], []


class Agents:
    """List of agents, same type different positions."""

    def __init__(self, agent_type, positions):
        """Agents object.

        agent_type: zombie or human.
        positions: spawn locations of agent.
        """
        self.agent_type = agent_type
        self.positions = positions
