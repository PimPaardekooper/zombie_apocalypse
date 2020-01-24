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

import random
import sys

class Apocalypse(Model):
    def __init__(self, height=50, width=50, density=0.1, infected_chance=0.05,
                        map_id=5, city_id=0, province="", total_agents=0,
                        human_kill_agent_chance=0.6, seed=None, patient_zero=False,
                        incubation_time=3, server=None):

        # variables to get from model_params in server.py
        self.server = server
        self.height = height
        self.width = width
        self.density = density
        self.infected_chance = infected_chance
        self.carrier = 0
        self.infected = 0
        self.susceptible = 0
        self.recovered = 0
        self.total_agents = total_agents
        self.total = 0
        self.patient_zero = patient_zero
        self.human_kill_zombie_chance = human_kill_agent_chance
        self.incubation_time = incubation_time

        print(self.density, self.incubation_time, self.incubation_time, self.human_kill_zombie_chance, self._seed)

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

        self.running = True
        self.datacollector.collect(self)


    def step(self):
        if (self.infected == 0 and self.carrier == 0) or (self.susceptible == 0):
            print(self.schedule.steps)
#
            # print(self.schedule.steps)
            #
            self.running = False
            self.server.model.running = False

            # print(experiments)
            #
            # if self.server:
            #     self.server.reset_model()
            #
            #     len_z = len(experiments['zombie'])
            #     len_h = len(experiments['human'])
            #
            #     # 100 iterations were run
            #     if len_z + len_h == 100:
            #         # f = open("results.txt", "a")
            #         #
            #         # f.write(str(experiment) + "\n")
            #         #
            #
            #

        self.schedule.step()
        self.datacollector.collect(self)
