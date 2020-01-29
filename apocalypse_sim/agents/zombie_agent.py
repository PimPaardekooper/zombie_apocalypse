"""The zombie agent class for simulating zombies."""

from .agent import Agent


class ZombieAgent(Agent):
    """Our own ZombieAgent class, extends our own Agent class.

    Attributes:
        agent_type (string): String specifying the type of the agent.
        target (:obj:): Agent(of agent_type "human") which is currently the
                        zombie's target

    """

    def __init__(self, pos, model, fsm):
        """Initialize the zombie agent.

        Args:
            pos (tuple): Position of the agent.
            model (:obj:): The corresponding model of the agent.
            fsm (:obj:): Finite state machine for the behaviour of the agent.

        """
        super().__init__(pos, model, fsm)

        self.agent_type = "zombie"
        self.target = None
        self.model.infected += 1

        self.setVision(7)

    def nearest_brain(self, neighbours):
        """Create a vector to a target human the zombie is tracking.

        Finds the nearest uninfected human to the ZombieAgent by iterating
        through all given humans, and making a list of the humans with the
        smallest euclidian distance to the ZombieAgent. Based on this list and
        target of the zombie, the zombie will pick its new target. He will
        chase this new target.

        Args:
            neighbours (list): A list containing all nearby agents.

        Returns:
            (tuple): Position of the current target, if one is found
            None: If no nearby susceptible human was found

        """
        nearby_humans = [agent for agent in neighbours if
                         agent.agent_type == "human" and "Infected" not in
                         [state.name for state in agent.states]]
                         
        if len(nearby_humans) > 0:
            nearest = None

            for human in nearby_humans:
                distance = ((abs(human.pos[0] - self.pos[0])**2 +
                             abs(human.pos[1] - self.pos[1])**2))**0.5
                if not nearest:
                    nearest = [distance, [human]]
                elif distance < nearest[0]:
                    nearest = [distance, [human]]
                elif distance == nearest[0]:
                    nearest[1].append(human)

            # If your target is not in list of nearest humans, pick a new
            # target
            if (not (self.target and self.target in nearest[1])):
                self.target = self.random.choice(nearest[1])

            return self.target.pos

        return None

    def move(self):
        """Move a zombie agent to the best possible cell.

        Moves the ZombieAgent to a cell. The cell is random if there is no
        human in range, otherwise the zombie will track the human, and the cell
        is the one closest to the human.

        """
        neighbours = self.model.grid.get_neighbors(self.pos, True, True,
                                                   self.traits["vision"])
        nearest_human = self.nearest_brain(neighbours)

        if nearest_human:
            new_cell = self.best_cell([nearest_human[0], nearest_human[1]])
        else:
            new_cell = self.random.choice(self.get_moves())

        self.model.grid.move_agent(self, new_cell)

    def setVision(self, visionRadius):
        """Set the vision radius for a human agent.

        Args:
            vision_radius (int): Radius how far a zombie can see.

        """
        self.traits["vision"] = min(9, visionRadius)
