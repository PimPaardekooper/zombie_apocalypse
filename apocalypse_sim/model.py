"""model.py

Creates the model for the computational experiment that needs to run.
"""
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import SingleGrid
from mesa.datacollection import DataCollector

class ApocalypseAgent(Agent):
    def __init__(self, pos, model, type, properties):
        super().__init__(pos, model)
        self.type = type
        self.pos = pos
        self.properties = properties

    def step(self):
        # get neighbours within vision(later make vision a property of an agent?)
        vision = 5;
        neighbours = self.model.grid.get_neighbors(self.pos, False, radius=self.properties["vision"])

        # print the neighbours for debugging purposes
        neigh = ""
        for n in neighbours:
            neigh += "(" + str(n.pos) + ", " + self.type + "), "
        print("(" + str(self.pos) + ", " + self.type + ") " + "neighbours: " + neigh)

        # until an AI is implemented, move the agent to a completely random
        # square in the grid
        self.model.grid.move_to_empty(self)


class Apocalypse(Model):
    def __init__(self, height=100, width=100, density=0.1, infected=0.05):
        # variables to get from model_params in server.py
        self.height = height
        self.width = width
        self.density = density
        self.infected = infected


        # NOTE: no idea what this does
        self.schedule = RandomActivation(self)
        self.grid = SingleGrid(height, width, torus=True)

        self.datacollector = DataCollector(
            {"type": "zombie"},  # Model-level count of zombie agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})
        # NOTE: end of weird stuff


        # All agents are created here
        for cell in self.grid.coord_iter():
            x = cell[1]
            y = cell[2]
            if self.random.random() < self.density:
                if self.random.random() < self.infected:
                    new_agent = ApocalypseAgent((x, y), self, "zombie", properties={"vision" : 4})
                else:
                    new_agent = ApocalypseAgent((x, y), self, "human", properties={"vision" : 5})

                self.grid.position_agent(new_agent, (x, y))
                self.schedule.add(new_agent)


        # NOTE: no idea what this does
        self.running = True
        self.datacollector.collect(self)
        # NOTE: end of weird stuff


    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
