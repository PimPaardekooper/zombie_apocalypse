from .agent import Agent

class HumanAgent(Agent):
    def __init__(self, pos, model, fsm, place=None):
        super().__init__(pos, model, fsm, place)
        self.setVision(4)
        self.type = "human"
        self.model.susceptible += 1

    def running_direction(self, nearby_zombies):
        # Get the optimal escape route by checking all zombie positions and
        # getting the route away from all zombies
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

    # For every free cell, calculates the priority for moving to the cell, and
    # returns the cell with the highest priority.
    # The priority is determined by adding the squared distances between the
    # cell and zombies.
    def bruteforce(self, nearby_zombies):
        # all available cells
        free_cells = self.get_moves()
        # list with priority of the highest priority cells, and the
        # corresponding cells
        best_cells = None

        if len(nearby_zombies) > 0:
            # Get the best possible cells
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
            # Pick a random cell out of the best options
            choice = self.random.choice(best_cells[1])

            # Create a normalized vector for the direction the agent wants to
            # go
            vector = [choice[0] - self.pos[0], choice[1] - self.pos[1]]
            length = (vector[0]**2 + vector[1]**2)**0.5
            if vector[0]:
                vector[0] /= length
            if vector[1]:
                vector[1] /= length
            return vector
        else:
            return None

    def find_escape(self, neighbours):
        nearby_zombies = [agent for agent in neighbours if agent.type == "zombie"]

        vector = self.running_direction(nearby_zombies)
        if vector:
            # If the vector doesnt find an escape route(agent stands still),
            # try the bruteforce algorithm.
            new_x = self.pos[0] + vector[0]
            new_y = self.pos[1] + vector[1]
            new_cell = self.best_cell([new_x, new_y])
            if new_cell == self.pos:
                vector = self.bruteforce(nearby_zombies)
            return vector


    def move(self):
        neighbours = self.model.grid.get_neighbors(self.pos, True, True, self.traits["vision"])
        direction = self.find_escape(neighbours, 1)

        if direction:
            # Calculate the coordinate the agent wants to move to
            new_x = self.pos[0] + direction[0]
            new_y = self.pos[1] + direction[1]
            new_cell = self.best_cell([new_x, new_y])

            # No move found using the fast algorithm, try the slower
            # bruteforce algorithm
            if new_cell == self.pos:
                direction = self.find_escape(neighbours, 2)
                new_x = self.pos[0] + direction[0]
                new_y = self.pos[1] + direction[1]
                new_cell = self.best_cell([new_x, new_y])
        else:
            # Randomly select a new cell to move to
            new_cell = self.random.choice(self.get_moves())

        # Move the agent to the selected cell
        self.model.grid.move_agent(self, new_cell)


    def setVision(self, vision_radius):
        self.traits['vision'] = min(9, vision_radius)


    def __del__(self):
        self.model.susceptible -= 1
