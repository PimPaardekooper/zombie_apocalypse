from matplotlib.path import Path
from copy import deepcopy
from mesa import Agent as MesaAgent
from math import floor, ceil

from shapely.geometry import Polygon, Point


class MapObjectAgent(MesaAgent):
    def __init__(self, pos, agent_type, model):
        super().__init__(pos, model)

        self.type = agent_type


class MapObject:
    def __init__(self, vertices):
        self.poly = Polygon(vertices)

    def __str__(self):
        return "None"

    def get_coords(self):
        min_x, min_y, max_x, max_y = self.poly.bounds

        xs = [x for x in range(floor(min_x), ceil(max_x))]
        ys = [y for y in range(floor(min_y), ceil(max_y))]

        return [(x,y) for y in ys for x in xs if self.poly.intersects(Point(x,y))]

class Place(MapObject):
    def __init__(self, vertices, population_density,
                 human_speed=2, zombie_speed=1):
        super().__init__(vertices)
        self.population_density = population_density
        self.human_speed = human_speed
        self.zombie_speed = zombie_speed

    def __str__(self):
        return "Place"

    def density_to_amount(self, density):
        return ceil(len(self.get_coords()) * density)

class Road(MapObject):
    def __init__(self, vertices, direction, speed):
        """
        NOTE:: Dir always positive.
        """
        super().__init__(vertices)
        self.direction = direction
        self.speed = speed

    def flip(self, pos):
        x, y = pos

        xs = self.poly.exterior.coords.xy[0]
        ys = self.poly.exterior.coords.xy[1]


        new_dir = [self.direction[0], self.direction[1]]

        if min([abs(max(xs) - x), abs(min(xs) - x)]) == abs(max(xs) - x):
            new_dir[0] = -new_dir[0]

        if min([abs(max(ys) - y), abs(min(ys) - y)]) == abs(max(ys) - y):
            new_dir[1] = -new_dir[1]

        return tuple(new_dir)

    def __str__(self):
        return "Road"
