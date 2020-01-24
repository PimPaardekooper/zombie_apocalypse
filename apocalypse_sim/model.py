"""
Creates the model for the computational experiment that needs to run.
"""
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from matplotlib.path import Path
from agents.human_agent import HumanAgent
from agents.zombie_agent import ZombieAgent
from agents.map_object import MapObjectAgent

from agents.map_gen import MapGen

class Apocalypse(Model):
    def __init__(self, height=100, width=100, density=0.1, infected_chance=0.05,
                        map_id=5, city_id=0, province="", total_agents=0,
                        human_kill_agent_chance=0.6, seed=0, patient_zero=False,
                        grouping=True, zombie_vision=7, human_vision=4):
        self._seed = seed

        # variables to get from model_params in server.py
        self.height = height
        self.width = width
        self.density = density
        self.infected_chance = infected_chance
        self.infected = 0
        self.susceptible = 0
        self.recovered = 0
        self.locked = []
        self.total_agents = total_agents
        self.total = 0
        self.patient_zero = patient_zero
        self.human_kill_zombie_chance = human_kill_agent_chance
        self.grouping = grouping
        self.zombie_vision = zombie_vision
        self.human_vision = human_vision

        # NOTE: no idea what this does
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=False)

        self.datacollector = DataCollector(
            {"infected": "infected",
             "susceptible": "susceptible",
             "recovered": "recovered",
             "reproductive_number": "reproductive_number"},  # Model-level count of zombie agents
            # For testing purposes, agent's individual x and y
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})
        # NOTE: end of weird stuff

        self.map = MapGen(map_id, city_id, infected_chance, province, self)

        # NOTE: no idea what this does
        self.running = True
        self.datacollector.collect(self)

        # NOTE: end of weird stuff

    def step(self):
        self.schedule.step()
        self.datacollector.collect(self)
