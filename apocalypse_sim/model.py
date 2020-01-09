"""model.py

Creates the model for the computational experiment that needs to run.
"""
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from matplotlib.path import Path
from human_agent import HumanAgent
# from ZombieAgent import ZombieAgent

class Apocalypse(Model):
    def __init__(self, height=100, width=100, density=0.1, infected=0.05):
        # variables to get from model_params in server.py
        self.height = height
        self.width = width
        self.density = density
        self.infected = infected

        # NOTE: no idea what this does
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=False)

        # self.datacollector = DataCollector(
        #     {"type": "zombie"},  # Model-level count of zombie agents
        #     # For testing purposes, agent's individual x and y
        #     {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})
        # NOTE: end of weird stuff

        # All agents are created here
        self.initial_map()
        # self.second_map()

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

            agent = HumanAgent((x, y), self)
            self.grid.place_agent(agent, (x, y))
            self.schedule.add(agent)

            # if self.random.random() < self.density:
            #     # NOTE: aanpassen equality naar <
            #     if self.random.random() >= self.infected:
            #

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

        village = Place(0.1, [[5,5],[10,5],[10,10],[5, 10],[5,5]])
        road = Place(0, [[8, 10] , [10, 8], [52, 50], [50, 52], [8, 10]])

        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]

            added = False

            for place in [city, village]:
                if place.path.contains_point((x, y)):
                    added = True

                    if self.random.random() < place.population_density:
                        properties = {}
                        if self.random.random() < self.infected:
                            properties["vision"] = 4
                            agent_type = "zombie"
                        else:
                            properties["vision"] = 5
                            agent_type = "human"

                        new_agent = HumanAgent((x, y), self, agent_type, properties=properties)
                        self.grid.place_agent(new_agent, x, y)
                        self.schedule.add(new_agent)
                    break


            if not added:
                for r in [road]:
                    if r.path.contains_point((x, y), radius=1):
                        added = True
                        break

            if not added:
                new_agent = HumanAgent((x, y), self, "wall", properties={})
                self.grid.place_agent(new_agent, (x, y))
                self.schedule.add(new_agent)




class Place:
    def __init__(self, population_density, vertices):
        self.population_density = population_density
        self.path = Path(vertices)

    # def inside_square(self, x, y):
        # return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2
