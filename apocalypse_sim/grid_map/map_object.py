"""map_object.py.

Map object represent the shape of places and roads and can give attributes
to these places which can then change the agents attributes.
"""
from matplotlib.path import Path
from copy import deepcopy
from mesa import Agent as MesaAgent
from math import floor, ceil

from shapely.geometry import Polygon, Point


class MapObjectAgent(MesaAgent):
    """Hold all immovable agents as a Mesa Agent."""

    def __init__(self, pos, agent_type, model, color=""):
        """MapObjectAgent.

        Args:
            pos (tuple): Spawn location agent.
            agent_type (string): Human or zombie.
            model (:obj:): Model object holds all needed information.
            color (string): Display color agent.

        """
        super().__init__(pos, model)

        self.agent_type = agent_type
        self.color = color


class MapObject:
    """Map object represented by a polygon and a color."""

    def __init__(self, vertices, color=""):
        """MapObject.

        Args:
            vertices (list): Vertices that make up the polygon.
            color (string): Display color.

        """
        self.poly = Polygon(vertices)
        self.color = color

    def get_coords(self):
        """Return all coordinates in the polygon.

        Returns:
            (list): List of all coordinated in polygon.

        """
        min_x, min_y, max_x, max_y = self.poly.bounds

        xs = [x for x in range(floor(min_x), ceil(max_x))]
        ys = [y for y in range(floor(min_y), ceil(max_y))]

        return [(x, y) for y in ys for x in xs
                if self.poly.intersects(Point(x, y))]


class Place(MapObject):
    """A map object that can change attributes of the agent within it."""

    def __init__(self, vertices, population_density, name="", color=""):
        """Subclass MapObject, Place.

        Args:
            vertices (list): Vertices that make up the polygon.
            population_density (float): Percentage of map has agents.
            name (string): String id (province name).
            color (string): Display color.

        """
        super().__init__(vertices, color=color)

        self.population_density = population_density
        self.name = name

    def __str__(self):
        """Represent object as string.

        Returns:
            (string): String representing object when printing it.

        """
        return "PlaceObject"

    def density_to_amount(self, density):
        """Convert the density to a value given the place area.

        Returns:
            (int): Density converted to an actual amount of agents.

        """
        return ceil(len(self.get_coords()) * density)


class Road(MapObject):
    """Move all agents within in a certain direction with a certain speed."""

    def __init__(self, vertices, direction, speed):
        """Subclass MapObject, Road.

        Args:
            vertices (list): Vertices that make up the polygon.
            direction (list): Direction agents need to walk when on the road.
            speed (int): How many cells in one step the agent takes.

        """
        super().__init__(vertices)

        self.direction = direction
        self.speed = speed

    def flip(self, pos):
        """Flip road direction given the start position of an agent.

        Check if an agent enters the road from the left, right top or bottom,
        by seeing if it is close to the maximum or minimum x and y value of
        the road and flip the sign for the direction accordingly.

        Args:
            pos (tuple): Position of agent.

        Returns:
            (tuple): Tuple containing new direction.

        """
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
        """Represent object as string.

        Returns:
            (string): String representing object when printing it.

        """
        return "RoadObject"
