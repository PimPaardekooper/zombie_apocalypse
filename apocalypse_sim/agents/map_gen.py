from .human_agent import HumanAgent
from .zombie_agent import ZombieAgent
from .map_object_agent import MapObjectAgent
from .map_object import Place, Road


class MapGen:
    def __init__(self, map_id, model):
        self.model = model

        maps = [self.initial_map, self.second_map, self.third_map, self.fourth_map]

        maps[map_id]()

        self.places, self.roads = maps[map_id]()

        print(self.paths_overlap(self.places))

        self.spawn_agents()

    def initial_map(self):
        """Square map no walls."""
        city = Place([[0, 0],
                      [0, self.model.grid.height],
                      [self.model.grid.width,
                       self.model.grid.height],
                      [self.model.grid.width, 0],
                      [0, 0]],
                     self.model.density)

        return [city], []

    def second_map(self):
        """
        Map that has a city and village and a road between. Every point that is
        not inside it you can't walk.
        """
        city = Place([[50, 75],
                      [75, 75],
                      [75, 50],
                      [50, 50],
                      [50, 75]],
                     0.3)

        village = Place([[5, 5], [10, 5], [10, 10], [5, 10], [5, 5]], 0.1)

        road = Road([[8, 10], [10, 8], [52, 50], [50, 52], [8, 10]], (1, 1), 2)

        return [city, village], [road]

    def third_map(self):
        """
        Map that has no roads.
        """
        city = Place([[50, 75],
                      [75, 75],
                      [75, 50],
                      [50, 50],
                      [50, 75]],
                     0.3)

        village = Place([[49, 70], [49, 55], [
                        30, 55], [30, 70], [49, 70]],
                        0.1)

        return [city, village], []


    def fourth_map(self):
        city1 = Place([[35, 35], [35,65],[65,65],[65,35],[35,35]], 0.3)

        city2 = Place([[15, 15], [15,25],[25,25],[25,15],[15,15]], 0.3)
        city3 = Place([[75, 75], [75,85],[85,85],[85,75],[75,75]], 0.3)
        city4 = Place([[15, 75], [15,85],[25,85],[25,75],[15,75]], 0.3)
        city5 = Place([[75, 15], [85,15],[85,25],[75,25],[75,15]], 0.3)

        road = Road([[23, 25], [25, 22], [37, 35], [35, 37], [23, 25]], (1, 1), 2)

        road2 = Road([[77, 75], [75, 77], [60, 62], [62, 60], [77, 75]], (1, 1), 2)

        # TODO:: symmetric if matplotlib.path is fixed
        road3 = Road([[77, 25], [75, 22], [62, 35], [65, 36], [77, 25]], (1, 1), 2)

        road4 = Road([[25, 77], [22, 75], [35, 61], [37, 65], [25, 77]], (1, 1), 2)

        return [city1, city2, city3, city4, city5], [road, road2, road3, road4]

    def spawn_agents(self):
        # TODO:: Edges path not right
        """Spawn agents like humans and cities.

        Loops through the grid coordinates and if a coordinate is part of a
        place it has a chance to spawn a agent and that agent has a chance to
        be infected. On that same coordinate is also a place agent spawned.

        If the coordinate doesn't contain a place it checks if it needs to spawn
        a road agent. If also isn't a road a wall agent is spawned.
        """
        for cell in self.model.grid.coord_iter():
            x = cell[1]
            y = cell[2]

            added = False

            for place in self.places:
                if place.path.contains_point((x, y)):
                    added = True

                    if self.model.random.random() < place.population_density:
                        properties = {}
                        properties["place"] = place

                        if self.model.random.random() < self.model.infection_change:
                            # properties["vision"] = 4
                            new_agent = ZombieAgent((x, y), self.model, place)
                            self.model.infected += 1
                        else:
                            new_agent = HumanAgent((x, y), self.model, place)
                            self.model.susceptible += 1

                        self.model.grid.place_agent(new_agent, (x, y))
                        self.model.schedule.add(new_agent)

                    new_agent = MapObjectAgent((x, y), "city", self.model)

                    self.model.grid.place_agent(new_agent, (x, y))
                    break

            if not added:
                for r in self.roads:
                    if r.path.contains_point((x, y)):
                        added = True
                        new_agent = MapObjectAgent((x, y), "road", self.model)
                        self.model.grid.place_agent(new_agent, (x, y))
                        break

            if not added:
                new_agent = MapObjectAgent((x, y), "wall", self.model)
                self.model.grid.place_agent(new_agent, (x, y))

    def get_place(self, pos):
        """Return place of current position."""
        for place in self.places + self.roads:
            if place.path.contains_point(pos):
                return place

        return False

    def paths_overlap(self, places):
        """Check if the places don't overlap."""
        for place in places:
            for place2 in places:
                if place != place2:
                    if place.path.intersects_path(place2.path):
                        return True

        return False


