from mesa import Model
from mesa import Agent as MesaAgent
from .map_object import Road
from shapely.geometry import Point

class Agent(MesaAgent):
    """
    Our own Agent class, this extends the agent class from the mesa framework.

    Args:
        pos (tuple): Position of the agent.
        model (:obj:): The corresponding model of the agent.
        fsm (:obj:): Finite state machine for the behaviour of the agent.

    Attributes:
        states (list): Keep track of the current states for the finite state
                       machine used to program agent behaviour.
        traits (dict): Information about properties of the agent, how far it
                       can see, for example.
        fsm (:obj:): The finite state machine that defines the agents behaviour
                     pos (tuple): The agents position.
        time_alive (int): The amount of steps an agent has been alive for.
        agent_type (string): String specifying the type of the agent.
        model (:obj:): The model an agent is spawned in.
    """
    def __init__(self, pos, model, fsm):
        super().__init__(model.total, model)

        self.states = []
        self.traits = {}
        self.fsm = fsm
        self.pos = pos
        self.time_alive = 0
        self.agent_type = ""
        self.model = model
        # Add one to the counter of total agents in the model
        self.model.total += 1



    def get_moves(self):
        """
        Check the cells that an agent is able to move to. Gets all non-occupied
        cells 1 space around the agent.

        Returns:
            (list): List containing all free cells an agent can move to.
        """
        grid = self.model.grid
        # List of agents we can't overlap with
        no_overlap = ["wall", "human", "zombie"]

        # Always give the option to stay on your current location(stand still)
        all_cells = self.neighbors()
        free_cells = [self.pos]

        # Get rid of cells that we may not move to by iterating through all
        # cells next to the agent, and only adding non-occupied cells
        for cell in all_cells:
            cell_occupied = False
            x, y = cell.pos
            # If there are agents in the current cell, and we are not allowed
            # to overlap with any of those agents, the cell is occupied.
            # Only add cells which are not occupied.
            if not grid.is_cell_empty((x, y)):
                for agent in grid[x][y]:
                    if agent.agent_type in no_overlap:
                        cell_occupied = True
                        break
            if not cell_occupied:
                free_cells.append((x, y))

        return free_cells



    def best_cell(self, coord):
        """
        Gets the nearest available cell of a coordinate by iterating through
        all available cells, and getting the cell where the euclidian distance
        to the given coordinate is the smallest.

        Args:
            coord (tuple): Tuple containing a (x, y) coordinate.

        Returns:
            (tuple): Tuple containing the nearest available cell to coord.
        """
        if coord[0] == self.pos[0] and coord[1] == self.pos[1]:
            return self.pos

        # Get all available cells
        free_cells = self.get_moves()
        smal_dist = float("Inf")

        for cell in free_cells:
            d_x = abs(coord[0] - cell[0])
            d_y = abs(coord[1] - cell[1])
            dist = (d_x**2 + d_y**2)**0.5
            if dist < smal_dist:
                smal_dist = dist
                new_cell = cell

        return new_cell



    def remove_agent(self):
        """
        Removes an agent of the grid.
        """
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

        if self.agent_type == "zombie":
            self.model.infected -= 1
        elif self.agent_type == "human":
            self.model.susceptible -= 1

        del self



    def neighbors(self, moore=True, include_center=True, radius=1):
        """
        Get the direct neighbours of an agent.

        Args:
            moore=True (bool): If true, get diagonal neighbours as well.
            include_center=True (bool): Include self if true.
            radius=1 (int): Range in which neighbours can be found.

        Returns:
            (list): List of direct neighbours.
        """
        return self.model.grid.get_neighbors(self.pos, moore, include_center, radius)



    def step(self):
        """
        Executes one step for an agent
        """
        self.time_alive += 1

        self.fsm.update(self)

        for state in self.states:
            if not self.pos:
                continue

            state.on_update(self)
