from .agent import Agent

class HumanAgent(Agent):
    """
    Our own HumanAgent class, extends our own Agent class.

    Args:
        pos (tuple): Position of the agent.
        model (:obj:): The corresponding model of the agent.
        fsm (:obj:): Finite state machine for the behaviour of the agent.

    Attributes:
        agent_type (string): String specifying the type of the agent.
        direction (tuple): The current direction where the HumanAgent is going.
    """
    def __init__(self, pos, model, fsm):
        super().__init__(pos, model, fsm)
        self.agent_type = "human"
        self.direction  = (0, 0)
        # Add one to the counter of total susceptible humans in the model
        self.model.susceptible += 1
        # Set vision range to 4
        self.setVision(4)



    def running_direction(self, nearby_zombies):
        """
        Get the direction for a zombie by creating a vector away from each
        zombie, this vector is scaled by the distance to the zombie.

        Args:
            nearby_zombies (list): list of zombies the HumanAgent can see.

        Returns:
            (tuple): Tuple containing the x and y coordinate of the direction
                     for the human, if a direction is found.
            None: If no direction was found.
        """
        direction = [0, 0]
        if len(nearby_zombies) > 0:
            for zombie in nearby_zombies:

                # Difference between the human and the zombie. This is the way
                # the human has to move to run away from the zombie
                d_x = float(self.pos[0]) - float(zombie.pos[0])
                d_y = float(self.pos[1]) - float(zombie.pos[1])

                # Normalize the way the human wants to run by the distance
                # between the human and the zombie(where a smaller distance
                # gives a higher direction x and y, since closer zombies have
                # priority)
                d = (d_x**2 + d_y**2)**0.5
                direction[0] += ((self.traits["vision"] + 1 - d) * d_x)
                direction[1] += ((self.traits["vision"] + 1 - d) * d_y)
        else:
            return None

        # Normalize the direction vector that was found
        d = (direction[0]**2 + direction[1]**2)**0.5
        if direction[0]:
            direction[0] /= d
        if direction[1]:
            direction[1] /= d
        return (direction[0], direction[1])



    def bruteforce(self, nearby_zombies):
        """
        For every free cell, calculates the priority for moving to the cell,
        and returns the cell with the highest priority.
        The priority is determined by adding the squared distances between the
        cell and zombies.

        Args:
            nearby_zombies (list): list of zombies the HumanAgent can see.

        Returns:
            (tuple): Tuple containing the x and y coordinate of the direction
                     for the human.
            None: If no direction was found.
        """
        free_cells = self.get_moves()
        best_cells = None

        # Iterate through all available cells and get the best one by checking
        # which one has the lowest root distance to all zombies
        if len(nearby_zombies) > 0:
            for cell in free_cells:
                priority = 0
                for zombie in nearby_zombies:
                    dist_x = abs(cell[0] - zombie.pos[0])
                    dist_y =  abs(cell[1] - zombie.pos[1])
                    distance = (dist_x**2 + dist_y**2)**0.5
                    priority += distance**0.5
                if not best_cells:
                    best_cells = [priority, [cell]]
                elif priority > best_cells[0]:
                    best_cells = [priority, [cell]]
                elif priority == best_cells[0]:
                    best_cells[1].append(cell)
            choice = self.random.choice(best_cells[1])

            # Create a normalized vector for the direction of the agent
            vector = [choice[0] - self.pos[0], choice[1] - self.pos[1]]
            length = (vector[0]**2 + vector[1]**2)**0.5
            if vector[0]:
                vector[0] /= length
            if vector[1]:
                vector[1] /= length
            return (vector[0], vector[1])
        else:
            return None



    def find_escape(self, neighbours):
        """
        Finds the best possible cell to go for a human agent. Do this by first
        trying the running_direction method. If the human is stuck, this method
        doesn't work and the bruteforce method is used.

        Args:
            neighbours (list): List of neighbours with a distance of 1.

        Returns:
            (tuple): Tuple containing the x and y coordinate of the direction
                     for the human.
            None: If no direction was found.
        """
        nearby_zombies = [agent for agent in neighbours if agent.agent_type == "zombie"]
        vector = self.running_direction(nearby_zombies)

        if vector:
            # If the vector doesnt find an escape route(agent stands still),
            # try the slower bruteforce algorithm.
            new_x = self.pos[0] + vector[0]
            new_y = self.pos[1] + vector[1]
            new_cell = self.best_cell([new_x, new_y])
            if new_cell == self.pos:
                vector = self.bruteforce(nearby_zombies)
            return vector
        return None



    def setVision(self, vision_radius):
        """
        Set the vision radius for a human agent.

        Args:
            vision_radius (int): Radius how far a human can see.
        """
        self.traits['vision'] = min(9, vision_radius)
