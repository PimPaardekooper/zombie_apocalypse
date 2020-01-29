"""State class for the states in a finite state machine."""

import sys
sys.path.append("..")

from .state import State
from agents.human_agent import HumanAgent
from agents.zombie_agent import ZombieAgent


class Reproduce(State):
    """Reproduction state.

    In this state two humans will try to reproduce to create a new human.

    Attributes:
        name (string): a string containing the name of the state.

    """

    def __init__(self):
        """Initialize the reproduce state."""
        self.name = "Reproduce"

    def reproduce(self, agent):
        """Let two agents reproduce.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (:obj:): If the agent has succesfully reproduced, return the
                     neighbour agent he has reproduced with.
            bool: Returns false if there is a zombie nearby, or if no viable
                  mating partner has been found, or if there was no place to
                  spawn a new human.

        """
        neighbours = agent.neighbors()

        for neighbour in neighbours:
            if neighbour.agent_type == "zombie":
                return False

        for neighbour in neighbours:
            birth_cells = agent.get_moves()[1:] + neighbour.get_moves()[1:]
            birth_cells = list(dict.fromkeys(birth_cells))

            if birth_cells:
                new_cell = agent.random.choice(birth_cells)
                new_agent = HumanAgent(new_cell, agent.model, agent.fsm)

                agent.model.grid.place_agent(new_agent, new_cell)
                agent.model.schedule.add(new_agent)

                return neighbour

        return False

    def transition(self, agent):
        """Check if an agent can transition into this state.

        An agent can transition into the current state if it has been alive for
        at least 3 steps, or if the time since the last reproduction is greater
        than 3 steps.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if the agent can transition into the current state,
                    false otherwise.

        """
        if "time_at_reproduction" in agent.traits:
            most_recent = agent.traits["time_at_reproduction"]

            return agent.time_alive - most_recent > 3

        return agent.time_alive > 3

    def on_update(self, agent):
        """Let an agent in this state execute one step.

        Let an agent reproduce. Set its time_alive as time it has last
        reproduced. (An agents time of last reproduction is relative to its
        time_alive)

        Args:
            agent (:obj:): The agent in the state.

        """
        if self.reproduce(agent):
            agent.traits["time_at_reproduction"] = agent.time_alive


class FormingHerd(State):
    """FormingHerd state.

    In this state agents will move towards other agents to form groups.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the FormingHerd state."""
        self.name = "FormingHerd"

    def transition(self, agent):
        """Check if an agent can transition into this state.

        An agent can transition into the current state if there is no zombie
        nearby, and there are 1 or more human(s) nearby.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if the agent can transition into the current state,
                    false otherwise.

        """
        human_count = 0

        for neighbour in agent.neighbors(include_center=False,
                                         radius=agent.traits["vision"]):
            if neighbour.agent_type == "zombie":
                return False

            if neighbour.agent_type == "human":
                human_count += 1

        if human_count > 0:
            return True

        return False

    def _normalize(self, vector):
        """Normalize a 2D list.

        Args:
            vector (list): A list containing a vector.

        Returns:
            (list): List containing the normalized vector.

        Note:
            Possibly make a helper function file containing helpers
            such as 'normalize'.

        """
        u = (vector[0] ** 2 + vector[1] ** 2) ** 0.5

        if u == 0:
            return vector

        vector[0] /= u
        vector[1] /= u

        return vector

    def alignment(self, agent, neighbors):
        """Make all agents move in the same direction.

        Args:
            agent (:obj:): Agent we want to know the direction for.
            neighbors (list): List containing the neighbouring agents.

        Returns:
            (list): List containing a normalized vector with the direction for
                    of an agent.

        """
        v = [0, 0]

        for neighbour in neighbors:
            v[0] += neighbour.direction[0]
            v[1] += neighbour.direction[1]

        v[0] /= len(neighbors)
        v[1] /= len(neighbors)

        return self._normalize(v)

    def cohesion(self, agent, neighbors):
        """Make all agents move towards the center of a group.

        Args:
            agent (:obj:): Agent we want to know the direction for.
            neighbors (list): List containing the neighbouring agents.

        Returns:
            (list): List containing a normalized vector with the direction for
                    of an agent.

        """
        v = [0, 0]

        for neighbour in neighbors:
            v[0] += neighbour.pos[0]
            v[1] += neighbour.pos[1]

        v[0] /= len(neighbors)
        v[1] /= len(neighbors)
        v[0] -= agent.pos[0]
        v[1] -= agent.pos[1]

        return self._normalize(v)

    def separation(self, agent, neighbors):
        """Make sure no agents interact with each other.

        Args:
            agent (:obj:): Agent we want to know the direction for.
            neighbors (list): List containing the neighbouring agents.

        Returns:
            (list): List containing a normalized vector with the direction for
                    of an agent.

        """
        v = [0, 0]

        # Negatate length to move away
        neigh_l = len(neighbors) * -1

        for neighbour in neighbors:
            v[0] += neighbour.pos[0] - agent.pos[0]
            v[1] += neighbour.pos[1] - agent.pos[1]

        v[0] /= neigh_l
        v[1] /= neigh_l

        return self._normalize(v)

    def direction(self, agent):
        """Get the direction vector an agent.

        Decides the direction for a human agent based on other agents in the
        area. This is used to simulate flocking behaviour.

        Args:
            agent (:obj:): Agent we want to know the direction for.

        Returns:
            (list): List containing a normalized vector with the direction for
                    of an agent.

        """
        neighbors = agent.neighbors(radius=agent.traits["vision"],
                                    include_center=False)
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
        """Let an agent in this state execute one step.

        Lets an agent move with the herd.

        Args:
            agent (:obj:): The agent in the state.

        """
        direction = self.direction(agent)

        # New cell to move to
        direction[0] += agent.pos[0]
        direction[1] += agent.pos[1]

        new_cell = agent.best_cell(direction)

        if new_cell[0] == agent.pos[0] and new_cell[1] == agent.pos[1]:
            a = agent.model.random.randrange(-1, 2)
            b = agent.model.random.randrange(-1, 2)
            new_cell = agent.best_cell((direction[0] + a, direction[1] + b))

        agent.direction = (new_cell[0] - agent.pos[0],
                           new_cell[1] - agent.pos[1])
        agent.model.grid.move_agent(agent, new_cell)


class Wandering(State):
    """Wandering state.

    In this state agents will wander around without any purpose.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the Wandering state."""
        self.name = "Wandering"

    def random_move(self, agent):
        """Move the agent to a randomly unoccupied cell around him.

        Args:
            agent (:obj:): The agent in the state.

        """
        free_cells = agent.get_moves()
        new_cell = agent.random.choice(free_cells)

        agent.model.grid.move_agent(agent, new_cell)

    def on_enter(self, agent):
        """Execute random_move when entering this state.

        Args:
            agent (:obj:): The agent in the state.

        """
        self.random_move(agent)

    def on_update(self, agent):
        """Execute random_move when on_update is called.

        Args:
            agent (:obj:): The agent in the state.

        """
        self.random_move(agent)


class FindDoor(State):
    """FindDoor state.

    In this state agents will attempt to find a door.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the FindDoor state."""
        self.name = "FindDoor"

    def get_best_cell(self, agent, target):
        """Get the cell nearest to the target."""
        return agent.best_cell([target[0], target[1]])

    def on_update(self, agent):
        if agent.pos in agent.model.door_coords:
            agent.fsm.switch_to_state(agent, self.name, "Escaped")
        else:
            best_cells = []

            for x in agent.model.door_coords:
                best_cells.append(self.get_best_cell(agent, x))

            best_cell = max(set(best_cells), key=best_cells.count)

            if best_cell:
                agent.direction = (best_cell[0] - agent.pos[0],
                                   best_cell[1] - agent.pos[1])

                agent.model.grid.move_agent(agent, best_cell)
            else:
                agent.direction = (0, 0)


class Escaped(State):
    """Escaped state.

    In this state agents have escaped.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the Escaped state."""
        self.name = "Escaped"

    def on_enter(self, agent):
        agent.remove_agent()

        del agent


class HumanWandering(Wandering):
    """HumanWandering state.

    In this state humans will wander around without any purpose.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the HumanWandering state."""
        self.name = "HumanWandering"

    def transition(self, agent):
        """Check if an agent can transition into this state.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if the agent can transition into the current state,
                    false otherwise.

        """
        neighbors = agent.neighbors(include_center=False,
                                    radius=agent.traits["vision"])

        # No humans (in grouping mode) or zombies nearby
        for neighbour in neighbors:
            if neighbour.agent_type == "zombie":
                return False

            if neighbour.agent_type == "human" and agent.model.grouping:
                return False

        return True


class ZombieWandering(Wandering):
    """ZombieWandering state.

    In this state zombies will wander around without any purpose.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the ZombieWandering state."""
        self.name = "ZombieWandering"

    def transition(self, agent):
        """Check if an agent can transition into this state.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if the agent can transition into the current state,
                    false otherwise.

        """
        neighbors = agent.neighbors(radius=agent.traits["vision"])

        return agent.nearest_brain(neighbors) is None


class AvoidingZombie(State):
    """AvoidingZombie state. In this state humans try to avoid zombies.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the AvoidingZombie state."""
        self.name = "AvoidingZombie"

    def get_best_cell(self, agent):
        """Find the best cell to move to.

        Find the best possible cell for an agent to move to, based
        on it's current neighbors.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (list): List containing the best possible cell.
            None: Returns None if no cell was found.

        """
        if not agent.pos:
            return None

        neighbors = agent.neighbors(radius=agent.traits["vision"])
        direction = agent.find_escape(neighbors)

        if direction:
            new_x = agent.pos[0] + direction[0]
            new_y = agent.pos[1] + direction[1]

            return agent.best_cell([new_x, new_y])

        return None

    def transition(self, agent):
        """Check if an agent can transition into this state.

        Only transition into this state if there are zombies within vision.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if the agent can transition into the current state,
                    false otherwise.

        """
        return self.get_best_cell(agent)

    def halt(self, agent):
        """Check if an agent is ready to leave the current state.

        Only leave the current state if there are not zombies within vision.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if an agent can transition into a different state,
                    false otherwise.

        """
        return self.get_best_cell(agent)

    def on_update(self, agent):
        """Let an agent in this state execute one step.

        Lets an agent run away from a zombie.

        Args:
            agent (:obj:): The agent in the state.

        """
        best_cell = self.get_best_cell(agent)

        if best_cell:
            agent.direction = (best_cell[0] - agent.pos[0],
                               best_cell[1] - agent.pos[1])

            agent.model.grid.move_agent(agent, best_cell)
        else:
            agent.direction = (0, 0)


class Idle(State):
    """Idle state. In this state zombies are not seeing any humans.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the Idle state."""
        self.name = "Idle"

    def transition(self, agent):
        """Check if an agent can transition into this state.

        Only transition into current state if not surrounded by
        any susceptible humans.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if the agent can transition into the current state,
                    false otherwise.

        """
        neighbors = agent.neighbors()

        for neighbour in neighbors:
            if neighbour.agent_type == "human":
                for state in neighbour.states:
                    if state.name == "Infected":
                        return False

        return True


class ChasingHuman(State):
    """ChasingHuman state. In this state zombies are actively chasing a human.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the ChasingHuman state."""
        self.name = "ChasingHuman"

    def get_best_cell(self, agent):
        """Get the best cell to chase a human.

        Gets the best cell to go by checking what human is the nearest, and
        then picking the nearest available cell to the human.

        Args:
            agent (:obj:): The zombie in the current state.

        Returns:
            (list): List containing the best possible cell.
            None: Returns none if no cell was found.

        """
        neighbors = agent.neighbors(radius=agent.traits["vision"])
        nearest_human = agent.nearest_brain(neighbors)

        if nearest_human:
            return agent.best_cell([nearest_human[0], nearest_human[1]])

        return None

    def transition(self, agent):
        """Check if an agent can transition into this state.

        Only transition into this state if there are humans within vision.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if the agent can transition into the current state,
                    false otherwise.

        """
        human = self.get_best_cell(agent)

        if human is None:
            return False

        neighbors = agent.neighbors()

        for neighbour in neighbors:
            if neighbour.agent_type == "human":
                for state in neighbour.states:
                    if state.name == "Infected":
                        return False

        return True

    def on_update(self, agent):
        """Let an agent in this state execute a step and move towards a human.

        Args:
            agent (:obj:): The agent in the state.

        """
        best_cell = self.get_best_cell(agent)

        if best_cell:
            agent.model.grid.move_agent(agent, best_cell)


class Susceptible(State):
    """Susceptible state. In this state humans are uninfected.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the Susceptible state."""
        self.name = "Susceptible"


class Infected(State):
    """Susceptible state. In this state humans are infected.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the Infected state."""
        self.name = "Infected"

    def transition(self, agent):
        """Check if an agent can transition into this state.

        Only transition into this state if its infected trait has been set in
        the Infect state.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if the agent can transition into the current state,
                    false otherwise.

        """
        return "infected" in agent.traits

    def on_enter(self, agent):
        """Update the counter and set infection time on entering this state.

        Args:
            agent (:obj:): The agent in the state.

        """
        agent.model.carrier += 1
        agent.traits["time_at_infection"] = agent.time_alive


class Turned(State):
    """Turned state.

    In this state humans are turned into a zombie.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the Turned state."""
        self.name = "Turned"

    def add_zombie(self, target):
        """Add a zombie to the simulation, and removes a human.

        Args:
            target (:obj:): agent to be removed

        """
        zombie = ZombieAgent(target.pos, target.model, target.fsm)

        target.model.grid.place_agent(zombie, target.pos)
        target.model.schedule.add(zombie)
        target.fsm.set_initial_states(["ZombieWandering", "Idle"], zombie)

    def transition(self, agent):
        """Check if an agent can transition into this state.

        Only transition into this state if a human has been infected for a
        certain amount of time.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if the agent can transition into the current state,
                    false otherwise.

        """
        return (agent.time_alive - agent.traits["time_at_infection"] >=
                agent.traits["incubation_time"])

    def on_enter(self, agent):
        """On entering this state, add a zombie and update counter.

        Args:
            agent (:obj:): The agent in the state.

        """
        self.add_zombie(agent)
        agent.remove_agent()

        agent.model.carrier -= 1


class InteractionHuman(State):
    """InteractionHuman state.

    In this state humans are being attacked by zombies.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the InteractionHuman state."""
        self.name = "InteractionHuman"

    def transition(self, agent):
        """Check if an agent can transition into this state.

        Only transition into this state if there are no zombies nearby, and
        there is another non-infected human in a neighbouring cell.

        Args:
            agent (:obj:): The agent in the state.

        Returns:
            (bool): True if the agent can transition into the current state,
                    false otherwise.

        """
        neighbors = agent.neighbors()

        for neighbour in neighbors:
            if not neighbour.agent_type == "human":
                continue

            for state in neighbour.states:
                if state.name == "Susceptible":
                    self.target = neighbour

                    return True

        return False

    def on_enter(self, agent):
        """Interact with nearby zombies when entering this state.

        When entering this state, the human gets a buff to the chance of
        defeating a zombie, based on how many other humans are near him. The
        human also gets a buff based on his total zombie kills. After the buff
        has been applied, the human can get infected. The buff can be at most
        50% when maxing out both nearby humans and kills.

        Args:
            agent (:obj:): The human in the current state.

        """
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
    """RemoveZombie state. In this state zombies are dead and will get removed.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the RemoveZombie state."""
        self.name = "RemoveZombie"

    def on_enter(self, agent):
        """When entering the state, update counter and remove the zombie.

        Args:
            agent (:obj:): The human in the current state.

        """
        agent.model.recovered += 1

        agent.remove_agent()

        del agent


class InfectHuman(State):
    """InfectHuman state. In this state zombies are trying to infect a human.

    Attributes:
        name (string): A string containing the name of the state.

    """

    def __init__(self):
        """Initialize the InfectHuman state."""
        self.name = "InfectHuman"

    def on_enter(self, agent):
        """Code to be executed upon entering this state.

        Attempt to find only susceptible humans, i.e. humans who do not
        already carry the virus. When entering the state, try to infect a
        human.

        Args:
            agent (:obj:): The zombie in the state.

        """
        neighbors = agent.neighbors()

        for neighbour in neighbors:
            if not neighbour.agent_type == "human":
                continue

            for state in neighbour.states:
                if state.name == "Susceptible":
                    neighbour.traits["infected"] = True

                    return
