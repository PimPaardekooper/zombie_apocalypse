from agents.human_agent import HumanAgent
from agents.zombie_agent import ZombieAgent
from agents.city_agent import BuildingAgent

from matplotlib.path import Path
from agents.automaton import Automaton
from agents.states import *


class MapGen:
    def __init__(self, map_id, model):
        self.model = model

        maps = [self.initial_map, self.second_map, self.third_map]

        maps[map_id]()

        self.places, self.roads = maps[map_id]()

        # print(self.paths_overlap(self.places))

        self.spawn_agents()

        # All agents are created here
        # self.initial_map()

        # Make different places on the map.
        # self.second_map()
        # self.third_map()

        # Initialize agent and map.

    def initial_map(self):
        city=Place(self.model.density, [[0, 0],
                            [0, self.model.grid.height],
                            [self.model.grid.width, self.model.grid.height],
                            [self.model.grid.width, 0],
                            [0, 0]])

        return [city], []
        # for cell in self.model.grid.coord_iter():
        #     x = cell[1]
        #     y = cell[2]

        #     if self.model.random.random() < self.density:
        #         if self.model.random.random() < self.infection_change:
        #             # properties["vision"] = 4
        #             new_agent = ZombieAgent((x, y), self.model.
        #             self.model.infected += 1
        #         else:
        #             new_agent = HumanAgent((x, y), self.model.
        #             self.model.susceptible += 1

        #         self.model.grid.place_agent(new_agent, (x, y))
        #         self.model.schedule.add(new_agent)

    def second_map(self):
        """
        Map that has a city and village and a road between. Every point that is
        not inside it you can't walk.
        """
        # TODO: path.contains_path, can't overlap.
        city=Place(0.3, [[50, 75],
                           [75, 75],
                           [75, 50],
                           [50, 50],
                           [50, 75]])

        city2=Place(0.3, [[50, 75],
                           [75, 75],
                           [75, 50],
                           [50, 50],
                           [50, 75]])

        village=Place(0.1, [[5, 5], [10, 5], [10, 10], [5, 10], [5, 5]])


        road=Place(0, [[8, 10], [10, 8], [52, 50], [50, 52], [8, 10]])

        return [city, village], [road]


    def third_map(self):
        """
        Map that has no roads.
        """
        city=Place(0.3, [[50, 75],
                           [75, 75],
                           [75, 50],
                           [50, 50],
                           [50, 75]])

        village=Place(0.1, [[49, 70], [49, 55], [30, 55], [30, 70], [49, 70]])



        return [city, village], []


    def spawn_agents(self):
        fsm = Automaton()

        fsm.event(Idle(), Tracking())

        for cell in self.model.grid.coord_iter():
            x = cell[1]
            y = cell[2]

            added = False

            for place in self.places:
                if place.path.contains_point((x, y), radius=-1):
                    added = True

                    if self.model.random.random() < place.population_density:
                        properties = {}
                        properties["place"] = place

                        if self.model.random.random() < self.model.infection_change:
                            # properties["vision"] = 4
                            new_agent = ZombieAgent((x, y), self.model, fsm)
                            print(x, y)
                            self.model.infected += 1
                        else:
                            print(x, y)
                            new_agent=HumanAgent((x, y), self.model, fsm)
                            self.model.susceptible += 1

                        self.model.grid.place_agent(new_agent, (x, y))
                        self.model.schedule.add(new_agent)

                    new_agent=BuildingAgent((x, y), "city", self.model, fsm)

                    self.model.grid.place_agent(new_agent, (x, y))
                    break


            if not added:
                for r in self.roads:
                    if r.path.contains_point((x, y), radius=1):
                        added=True
                        new_agent=BuildingAgent((x, y), "road", self.model, fsm)
                        self.model.grid.place_agent(new_agent, (x, y))
                        break

            if not added:
                new_agent=BuildingAgent((x, y), "wall", self.model, fsm)
                self.model.grid.place_agent(new_agent, (x, y))



    def get_place(self, pos):
        """Return place of current posiion."""
        for place in self.places + self.roads:
            if place.path.contains_point(pos):
               return place

    def paths_overlap(self, places):
        """Check if path mades don't overlap."""
        for place in places:
            for place2 in places:
                if place != place2:
                    if place.path.intersects_path(place2.path):
                        return True

        return False



class Place:
    def __init__(self, population_density, vertices):
        self.population_density=population_density
        self.path=Path(vertices)
