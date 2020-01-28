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

    def __init__(self, pos, agent_type, model, place=None, color=""):
        """MapObjectAgent.

        pos: spawn location agent.
        agent_type: city or road.
        model: Apocalypse object holds all needed information.
        color: display color agent.
        """
        super().__init__(pos, model)

        self.agent_type = agent_type
        self.color = color
        self.place = place


class MapObject:
    """Hold the map object that is represented by a polygon.

    Subclasses can be a Road with speed and direction or Place with a
    certain population density.
    """

    def __init__(self, vertices, color=""):
        """MapObject.

        vertices: vertices that make up the polygon.
        color: display color.
        """
        self.poly = Polygon(vertices)
        self.color = color

    def __str__(self):
        """Represent object as string."""
        return "None"

    def get_coords(self):
        """Return all coordinates in the polygon."""
        min_x, min_y, max_x, max_y = self.poly.bounds

        xs = [x for x in range(floor(min_x), ceil(max_x))]
        ys = [y for y in range(floor(min_y), ceil(max_y))]

        return [(x, y) for y in ys for x in xs
                if self.poly.intersects(Point(x, y))]


class Place(MapObject):
    """A map object that can change attributes of the agent within it."""

    def __init__(self, vertices, population_density, name="", color=""):
        """Subclass MapObject, Place.

        vertices: vertices that make up the polygon.
        population_density: percentage of map has agents.
        name: string id (province name).
        color: display color.
        """
        super().__init__(vertices, color=color)
        self.population_density = population_density
        self.name = name

    def __str__(self):
        """Represent object as string."""
        return "Place"

    def density_to_amount(self, density):
        """Convert the density to a value given the place area."""
        return ceil(len(self.get_coords()) * density)


class Road(MapObject):
    """Move all agents within in a certain direction with a certain speed."""

    def __init__(self, vertices, direction, speed):
        """Subclass MapObject, Road.

        vertices: vertices that make up the polygon.
        direction: direction agents need to walk when on the road.
        speed: how many cells in one step the agent takes.
        """
        super().__init__(vertices)
        self.direction = direction
        self.speed = speed

    def flip(self, pos):
        """Flip direction given start position.

        Check if a agent start the road from the left or right up or under,
        by seeing if it is close to the maximum or minimum x and y value of
        the road and flips the sign for the direction accordingly.
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
        """Represent object as string."""
        return "Road"
