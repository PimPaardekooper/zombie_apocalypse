"""model.py.

Creates the model where we will simulate a zombie outbreak.
"""
from mesa import Model, Agent
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from matplotlib.path import Path
from agents.human_agent import HumanAgent
from agents.zombie_agent import ZombieAgent
from grid_map.map_object import MapObjectAgent
from grid_map.map_gen import MapGen
from automaton.automaton import Automaton

import random
import sys


class Apocalypse(Model):
    """Apocalypse model.

    Model holds all the data and functions for the simulation to work. It is
    a subclass of the mesa framework.
    """

    def __init__(self, height=50, width=50, density=0.1, infected_chance=0.05,
                 map_id=5, city_id=0, province="", total_agents=0,
                 human_kill_agent_chance=0.6, patient_zero=False,
                 door_width=5, seed=None, incubation_time=3,
                 server=None):
        """Apocalypse object.

        Initializes the apocalypse object, makes the grid and put agents on
        that grid.

        height: grid height.
        width: grid_width
        density: percentage of the amount of agents in an area.
        infected_chance: change of agents in an area to be infected.
        map_id: index to choose from a list of maps in maps_layout.py.
        city_id: index of the city where the outbreak happens.
        province: in the holland map the province where the outbreak starts.
        total_agents: ??????????????????????????????????????????????????????????????????
        human_kill_agent_chance: chance for a human to kill a zombie.
        patient_zero: boolean if only on person should be infected.
        door_width: width of the door way.
        seed: seed that decides all randomness in the model, so you can repeat
            the exact same experiments.
        incubation_time: time it takes for a infected human to turn.
        server: ??????????????????????????????????????????????????????????????????????
        """
        # variables to get from model_params in server.py
        self._seed = seed
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
        self.door = [(-1, -1)]
        self.door_coords = []
        self.door_width = door_width
        self.incubation_time = incubation_time
        self.fsm = Automaton()

        print(self.density, self.incubation_time, self.incubation_time,
              self.human_kill_zombie_chance, self._seed)

        # Set agents step function in a schedule to be called in random order.
        self.schedule = RandomActivation(self)

        # Makes multigrid, grid which can hold multiple agents on one cell.
        self.grid = MultiGrid(width, height, torus=False)

        # Collects data each step and plots it in server.py.
        self.datacollector = DataCollector(
            {"infected": "infected",
             "susceptible": "susceptible",
             "recovered": "recovered"},
            {"x": lambda a: a.pos[0], "y": lambda a: a.pos[1]})

        # Creates agents and map layouts.
        self.map = MapGen(map_id, city_id, infected_chance, province, self)

        # If there is a door in the map you get the coordinates.
        if self.door[0] != (-1, -1):
            self.get_door_coords()

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """Step function.

        Call all agents and collect data, stop if there are no more zombies
        or no more humans.
        """
        if (self.infected == 0 and self.carrier == 0) or \
                (self.susceptible == 0):
            print(self.schedule.steps)
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

    def get_door_coords(self):
        """Door range to coordinates.

        Model gets a range for the door, this turns that into a list of
        coordinates and gives it to the model.
        """
        xs = range(self.door[0][0], self.door[1][0] + 1)
        ys = [self.door[0][1] for _ in range(len(xs))]
        self.door_coords = list(zip(xs, ys))
