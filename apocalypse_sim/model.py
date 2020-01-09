"""model.py

Creates the model for the computational experiment that needs to run.
"""
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from matplotlib.path import Path
from agents.human_agent import HumanAgent
from agents.zombie_agent import ZombieAgent

class Apocalypse(Model):
    def __init__(self, height=100, width=100, density=0.1, infection_change=0.05):
        # variables to get from model_params in server.py
        self.height = height
        self.width = width
        self.density = density
        self.infection_change = infection_change
        self.places = []
        self.roads = []

        self.infected = 0
        self.susceptible = 0

        # NOTE: no idea what this does
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=False)

        self.datacollector = DataCollector(
            {"infected": "infected",
             "susceptible": "susceptible"},  # Model-level count of zombie agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})
        # NOTE: end of weird stuff

        # All agents are created here
        self.initial_map()

        # Make different places on the map.
        # self.second_map()
        # self.third_map()

        # Initialize agent and map.
        # self.make_map()

        # NOTE: no idea what this does
        self.running = True
        # self.datacollector.collect(self)
        # NOTE: end of weird stuff

    def step(self):
        self.schedule.step()
        # self.datacollector.collect(self)


    # NOTE: Pim's map code
    def initial_map(self):
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]

            if self.random.random() < self.density:
                if self.random.random() < self.infection_change:
                    # properties["vision"] = 4
                    new_agent = ZombieAgent((x, y), self)
                    self.infected += 1
                else:
                    new_agent = HumanAgent((x, y), self)
                    self.susceptible += 1

                self.grid.place_agent(new_agent, (x, y))
                self.schedule.add(new_agent)

    def make_map(self):
        """Spawn map with place object in self.roades and self.places. Places with a population density will spawm agents."""

        print(self.paths_overlap(self.places))

        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]

            added = False

            for place in self.places:
                if place.path.contains_point((x, y)):
                    added = True

                    if self.random.random() < place.population_density:
                        properties = {}
                        properties["place"] = place

                        if self.random.random() < self.infection_change:
                            # properties["vision"] = 4
                            new_agent = ZombieAgent((x, y), self)
                            self.infected += 1
                        else:
                            new_agent = HumanAgent((x, y), self)
                            self.susceptible += 1

                        self.grid.place_agent(new_agent, (x, y))
                        self.schedule.add(new_agent)

                    new_agent = BuildingAgent((x, y), "city", self)

                    self.grid.place_agent(new_agent, (x, y))
                    break


            if not added:
                for r in self.roads:
                    if r.path.contains_point((x, y), radius=1):
                        added = True
                        new_agent = BuildingAgent((x, y), "road", self)
                        self.grid.place_agent(new_agent, (x, y))
                        break

            if not added:
                new_agent = BuildingAgent((x, y), "wall", self)
                self.grid.place_agent(new_agent, (x, y))

    def paths_overlap(self, places):
        """Check if path mades don't overlap."""
        for place in places:
            for place2 in places:
                if place != place2:
                    if place.path.intersects_path(place2.path):
                        return True

        return False

    def second_map(self):
        """
        Map that has a city and village and a road between. Every point that is
        not inside it you can't walk.
        """
        # TODO: path.contains_path, can't overlap.
        city = Place(0.3, [[50, 75],
                           [75, 75],
                           [75,50],
                           [50,50],
                           [50, 75]])

        city2 = Place(0.3, [[50, 75],
                           [75, 75],
                           [75,50],
                           [50,50],
                           [50, 75]])

        village = Place(0.1, [[5,5],[10,5],[10,10],[5, 10],[5,5]])


        road = Place(0, [[8, 10] , [10, 8], [52, 50], [50, 52], [8, 10]])

        self.places = [city, village]
        self.roads = [road]





    def third_map(self):
        """
        Map that has no roads.
        """
        city = Place(0.3, [[50, 75],
                           [75, 75],
                           [75,50],
                           [50,50],
                           [50, 75]])

        village = Place(0.1, [[49,70],[49,55],[30,55],[30, 70],[49,70]])



        self.places = [city, village]
        self.roads = []



    def get_place(self, pos):
        """Return place of current posiion."""
        for place in self.places + self.roads:
            if place.path.contains_point(pos):
                return place


class Place:
    def __init__(self, population_density, vertices):
        self.population_density = population_density
        self.path = Path(vertices)

    # def inside_square(self, x, y):
        # return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2
