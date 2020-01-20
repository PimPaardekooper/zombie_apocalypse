"""map_gen.py.

Spawns all map object and agents and schedules them.
"""
from .human_agent import HumanAgent
from .zombie_agent import ZombieAgent
from .map_object import Place, Road, MapObjectAgent
from .map_layouts import Map

from .automaton import Automaton
from .states import *
from math import floor, ceil
from mode import is_verification

from shapely.geometry import Polygon, Point

def getFsm():
    fsm = Automaton()

    # Zombie movement FSM
    fsm.event(ZombieWandering(), ChasingHuman())
    fsm.event(ChasingHuman(), ZombieWandering())

    # Zombie human interaction FSM
    fsm.event(Idle(), InteractionHuman())
    fsm.event(InteractionHuman(), InfectHuman())
    fsm.event(InteractionHuman(), RemoveZombie())
    fsm.event(InfectHuman(), Idle())

    # Human movement FSM
    fsm.event(HumanWandering(), AvoidingZombie())
    fsm.event(AvoidingZombie(), HumanWandering())

    # Human health FSM
    fsm.event(Susceptible(), Infected())
    fsm.event(Infected(), Turned())
    return fsm


class MapGen:
    """Hold a generated map and agents spawned within it."""

    def __init__(self, map_id, city_id, infected_chance, province, model):
        self.model = model

        self.map = Map(map_id, model)


        self.spawn_map()
        self.spawn_agents()
        if not is_verification():
            self.spawn_agents_in_city(city_id, infected_chance, province)

    def spawn_map(self):
        """Spawns map agents

        Loops through the grid and checks first if it is a place then a road and otherwise it spawns a wall.
        """
        for cell in self.model.grid.coord_iter():
            x = cell[1]
            y = cell[2]

            added = False

            for place in self.map.places:
                if place.poly.intersects(Point(x, y)):
                    added = True
                    new_agent = MapObjectAgent((x, y), "city", self.model, color=place.color)
                    self.model.grid.place_agent(new_agent, (x, y))
                    break

            if not added:
                for r in self.map.roads:
                    if r.poly.intersects(Point(x, y)):
                        added = True
                        new_agent = MapObjectAgent((x, y), "road", self.model)
                        self.model.grid.place_agent(new_agent, (x, y))
                        break

            if not added:
                new_agent = MapObjectAgent((x, y), "wall", self.model)
                self.model.grid.place_agent(new_agent, (x, y))


    def spawn_agents(self):
        """Spawn hard coded agents, good for situations."""
        for agent in self.map.agents:
            for pos in agent.positions:
                fsm = getFsm()
                if agent.agent_type == "zombie":
                    new_agent = ZombieAgent(pos, self.model, fsm, self.get_place(pos))
                    fsm.set_initial_states(["ZombieWandering", "Idle"], new_agent)
                    self.model.infected += 1
                else:
                    new_agent = HumanAgent(pos, self.model, fsm, self.get_place(pos))
                    fsm.set_initial_states(["HumanWandering", "Susceptible"], new_agent)
                    self.model.susceptible += 1

                self.model.grid.place_agent(new_agent, pos)
                self.model.schedule.add(new_agent)

    def spawn_agents_in_city(self, city_id, infected_chance, province):
        """Spawn agents like humans and zombies, defined by place densities.

        For each place it will calculate how much agents need to spawn given
        the place area and agent density. Then it will pick so much random coordinates
        from that place. From those coordinates a percentage will randomly be infected and
        spawns a ZombieAgent the rest will spawn as HumanAgents.
        """

        fsm = Automaton()

        # Zombie movement FSM
        fsm.event(ZombieWandering(), ChasingHuman())
        fsm.event(ChasingHuman(), ZombieWandering())

        # Zombie human interaction FSM
        fsm.event(Idle(), InteractionHuman())
        fsm.event(InteractionHuman(), InfectHuman())
        fsm.event(InteractionHuman(), RemoveZombie())
        fsm.event(InfectHuman(), Idle())

        # Human movement FSM
        fsm.event(HumanWandering(), AvoidingZombie())
        fsm.event(AvoidingZombie(), HumanWandering())

        # Human health FSM
        fsm.event(Susceptible(), Infected())
        fsm.event(Infected(), Turned())

        for c_id, place in enumerate(self.map.places):
            p_coords = place.get_coords()

            infected_coords = []
            agent_coords = self.model.random.sample(range(len(p_coords)),
                                         place.density_to_amount(place.population_density))

            if (province == "" and city_id == c_id) or (province == place.name):
                infected_coords = self.model.random.sample(agent_coords,
                                                ceil(len(agent_coords) * (infected_chance)))

            open('remove_add.txt', 'w').close()

            for i in agent_coords:
                pos = p_coords[int(i)]
                properties = {}
                properties["place"] = self.get_place(pos)

                if i in infected_coords:
                    new_agent = ZombieAgent(pos, self.model, fsm, place)

                    fsm.set_initial_states(["ZombieWandering", "Idle"], new_agent)
                else:
                    new_agent = HumanAgent(pos, self.model, fsm, place)

                    fsm.set_initial_states(["HumanWandering", "Susceptible"], new_agent)

                self.model.grid.place_agent(new_agent, pos)
                self.model.schedule.add(new_agent)

    def get_place(self, pos):
        """Return place of current position."""
        for place in self.map.places + self.map.roads:
            if place.poly.intersects(Point(pos)):
                return place

        return False


    def paths_overlap(self, places):
        """Check if the places don't overlap."""
        for place in places:
            for place2 in places:
                if place != place2:
                    if place.poly.intersects_path(place2.path):
                        return True

        return False
