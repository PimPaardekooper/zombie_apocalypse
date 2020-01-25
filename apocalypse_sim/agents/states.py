from .state import State
from .human_agent import HumanAgent
from .zombie_agent import ZombieAgent


class Reproduce(State):
    def reproduce(self, agent):
        neighbors = agent.neighbors()

        # Continue only if a human neighbour is found
        for neighbour in neighbors:
            if neighbour.agent_type != "human":
                return False

            if self.name in agent.states:
                birth_cells = agent.get_moves()

                if not birth_cells:
                    birth_cells = neighbour.get_moves()

                new_cell = agent.random.choice(birth_cells)

                new_agent = HumanAgent(new_cell, agent.model, agent.fsm, {})

                agent.model.grid.place_agent(new_agent, new_cell)
                agent.model.schedule.add(new_agent)

                return neighbour

        return False


    def __init__(self):
        self.name = "Reproduce"


    """
    An agent may transition into the current state if it has
    been alive for at least 3 steps, or the time since the
    last reproduction is greater than 3 steps.
    """
    def transition(self, agent):
        if "time_at_reproduction" in agent.traits:
            most_recent = agent.traits["time_at_reproduction"]

            return agent.time_alive - most_recent > 3

        return agent.time_alive > 3


    def on_update(self, agent):
        if self.reproduce(agent):
            agent.traits["time_at_reproduction"] = agent.time_alive


class FormingHerd(State):
    def __init__(self):
        self.name = "FormingHerd"


    def transition(self, agent):
        human_count = 0

        for neighbour in agent.neighbors(include_center=False, radius=agent.traits["vision"]):
            if neighbour.agent_type == "zombie":
                return False

            if neighbour.agent_type == "human":
                human_count += 1

        if human_count > 0:
            return True

        return False


    """
    Normalize a 2D list.
    Returns list.
    Note: Possibly make a helper function file containing helpers
    such as 'normalize'.
    """
    def _normalize(self, vector):
        u = (vector[0] ** 2 + vector[1] ** 2) ** 0.5

        if u == 0:
            return vector

        vector[0] /= u
        vector[1] /= u

        return vector


    """
    Make all agents move in the same direction.
    """
    def alignment(self, agent, neighbors):
        v = [0, 0]
        l = len(neighbors)

        for neighbour in neighbors:
            v[0] += neighbour.direction[0]
            v[1] += neighbour.direction[1]

        v[0] /= l
        v[1] /= l

        return self._normalize(v)


    """
    Make all agents move towards the center of a group.
    """
    def cohesion(self, agent, neighbors):
        v = [0, 0]
        l = len(neighbors)

        for neighbour in neighbors:
            v[0] += neighbour.pos[0]
            v[1] += neighbour.pos[1]

        v[0] /= l
        v[1] /= l

        v[0] -= agent.pos[0]
        v[1] -= agent.pos[1]

        return self._normalize(v)


    """
    Make sure no agents interact with each other.
    """
    def separation(self, agent, neighbors):
        v = [0, 0]

        # Negatate length to move away
        l = len(neighbors) * -1

        for neighbour in neighbors:
            v[0] += neighbour.pos[0] - agent.pos[0]
            v[1] += neighbour.pos[1] - agent.pos[1]

        v[0] /= l
        v[1] /= l

        return self._normalize(v)

    """
    Get the direction vector for every agent so that
    we can simulate flocking behaviour.
    """
    def direction(self, agent):
        neighbors = agent.neighbors(radius=agent.traits["vision"], include_center=False)
        humans = [human for human in neighbors if human.agent_type == "human"]

        # No humans nearby, do not move.
        if not humans:
            return [0, 0]

        alignment = self.alignment(agent, humans)
        cohesion = self.cohesion(agent, humans)
        separation = self.separation(agent, humans)

        direction = [
            alignment[0] + cohesion[0] + separation[0],
            alignment[1] + cohesion[1] + separation[1]
        ]

        return self._normalize(direction)


    def on_update(self, agent):
        direction = self.direction(agent)

        # New cell to move to
        direction[0] += agent.pos[0]
        direction[1] += agent.pos[1]

        new_cell = agent.best_cell(direction)

        if new_cell[0] == agent.pos[0] and new_cell[1] == agent.pos[1]:
            a = agent.model.random.randrange(-1, 2)
            b = agent.model.random.randrange(-1, 2)

            new_cell = agent.best_cell((direction[0] + a, direction[1] + b))

        agent.direction = (new_cell[0] - agent.pos[0], new_cell[1] - agent.pos[1])

        agent.model.grid.move_agent(agent, new_cell)


class Wandering(State):
    def __init__(self):
        self.name = "Wandering"


    def random_move(self, agent):
        free_cells = agent.get_moves()
        new_cell = agent.random.choice(free_cells)

        agent.model.grid.move_agent(agent, new_cell)


    def on_enter(self, agent):
        self.random_move(agent)


    def on_update(self, agent):
        self.random_move(agent)


class HumanWandering(Wandering):
    def __init__(self):
        self.name = "HumanWandering"


    def transition(self, agent):
        neighbors = agent.neighbors(include_center=False, radius=agent.traits["vision"])

        # No humans or zombies nearby
        for neighbour in neighbors:
            if neighbour.agent_type == "zombie" or neighbour.agent_type == "human":
                return False


        return True


class ZombieWandering(Wandering):
    def __init__(self):
        self.name = "ZombieWandering"


    def transition(self, agent):
        neighbors = agent.neighbors(radius=agent.traits["vision"])

        return agent.nearest_brain(neighbors) == None


class AvoidingZombie(State):
    def __init__(self):
        self.name = "AvoidingZombie"


    def get_best_cell(self, agent):
        if not agent.pos:
            return None

        neighbors = agent.neighbors(radius=agent.traits["vision"])
        direction = agent.find_escape(neighbors)

        if direction:
            # Calculate the coordinate the agent wants to move to
            new_x = agent.pos[0] + direction[0]
            new_y = agent.pos[1] + direction[1]

            return agent.best_cell([new_x, new_y])

        return None


    def transition(self, agent):
        return self.get_best_cell(agent)


    def halt(self, agent):
        return self.get_best_cell(agent)


    def on_update(self, agent):
        best_cell = self.get_best_cell(agent)

        if best_cell:
            agent.direction = (best_cell[0] - agent.pos[0], best_cell[1] - agent.pos[1])

            agent.model.grid.move_agent(agent, best_cell)
        else:
            agent.direction = (0, 0)


class Idle(State):
    def __init__(self):
        self.name = "Idle"


    """
    Only transition into current state if not surrounded by
    any susceptible humans.
    """
    def transition(self, agent):
        neighbors = agent.neighbors()

        for neighbour in neighbors:
            if neighbour.agent_type == "human":
                for state in neighbour.states:
                    if state.name == "Infected":
                        return False

        return True


class ChasingHuman(State):
    def __init__(self):
        self.name = "ChasingHuman"


    def get_best_cell(self, agent):
        neighbors = agent.neighbors(radius=agent.traits["vision"])
        nearest_human = agent.nearest_brain(neighbors)

        if nearest_human:
            return agent.best_cell([nearest_human[0], nearest_human[1]])

        return None


    def transition(self, agent):
        human = self.get_best_cell(agent)

        # If a human is not found in your vision, you can't
        # chase any, so you should go to the wandering state
        # instead.
        if human == None:
            return False

        # If a human is one block away you must infect him,
        # otherwise can chase him.
        neighbors = agent.neighbors()

        for neighbour in neighbors:
            if neighbour.agent_type == "human":
                for state in neighbour.states:
                    if state.name == "Infected":
                        return False

        # You are ready to chase someone
        return True


    def on_update(self, agent):
        best_cell = self.get_best_cell(agent)

        if best_cell:
            agent.model.grid.move_agent(agent, best_cell)


class Susceptible(State):
    def __init__(self):
        self.name = "Susceptible"


class Infected(State):
    def __init__(self):
        self.name = "Infected"


    """
    A human may transition into the Infected state if
    it's infected trait has been set in the Infect state.
    """
    def transition(self, agent):
        return "infected" in agent.traits


    def on_enter(self, agent):
        agent.model.carrier += 1

        agent.traits["time_at_infection"] = agent.time_alive


class Turned(State):
    def __init__(self):
        self.name = "Turned"


    def add_zombie(self, target):
        zombie = ZombieAgent(target.pos, target.model, target.fsm)

        target.model.grid.place_agent(zombie, target.pos)
        target.model.schedule.add(zombie)

        target.fsm.set_initial_states(["ZombieWandering", "Idle"], zombie)


    def transition(self, agent):
        return agent.time_alive - agent.traits["time_at_infection"] >= agent.traits["incubation_time"]


    def on_enter(self, agent):
        self.add_zombie(agent)
        agent.remove_agent()

        agent.model.carrier -= 1


class InteractionHuman(State):
    def __init__(self):
        self.name = "InteractionHuman"


    def transition(self, agent):
        neighbors = agent.neighbors()

        # Find any human that is not yet been infected
        for neighbour in neighbors:
            if not neighbour.agent_type == "human":
                continue

            for state in neighbour.states:
                if state.name == "Susceptible":
                    self.target = neighbour

                    return True

        return False


    def on_enter(self, agent):
        chance = agent.model.random.random()
        buff = 0

        if "zombie_kills" in self.target.traits:
            buff += min(self.target.traits["zombie_kills"] * 0.05, 0.3)
        else:
            self.target.traits["zombie_kills"] = 0


        neighbour_count = 0

        for neighbour in self.target.neighbors():
            if neighbour.agent_type == "human":
                neighbour_count += 1

        buff += min(neighbour_count * 0.05, 0.2)

        total = min(0.8, agent.model.human_kill_zombie_chance + buff)

        if chance <= total:
            agent.fsm.switch_to_state(agent, self.name, "RemoveZombie")

            self.target.traits["zombie_kills"] += 1
        else:
            agent.fsm.switch_to_state(agent, self.name, "InfectHuman")


class RemoveZombie(State):
    def __init__(self):
        self.name = "RemoveZombie"


    def on_enter(self, agent):
        agent.model.recovered += 1
        agent.remove_agent()

        del agent


"""
State that represents a zombie infecting a human.
"""
class InfectHuman(State):
    def __init__(self):
        self.name = "InfectHuman"


    """
    A zombie has spotted a nearby human and will 'infect' it by
    setting it's infected trait.
    """
    def on_enter(self, agent):
        neighbors = agent.neighbors()

        # Find any human that is susceptible to
        # being infected.
        for neighbour in neighbors:
            if not neighbour.agent_type == "human":
                continue

            for state in neighbour.states:
                if state.name == "Susceptible":
                    neighbour.traits["infected"] = True
                    return
