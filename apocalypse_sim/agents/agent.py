from mesa import Model
from mesa import Agent as MesaAgent

from .map_object import Road

class Agent(MesaAgent):
    def __init__(self, pos, model, place):
        super().__init__(pos, model)

        self.pos = pos
        self.traits = {}

        self.model = model

        self.place = place
        self.direction = (0, 0)
        self.on_road = False

    def get_moves(self):
        grid = self.model.grid
        no_overlap = ["wall", "human", "zombie"]

        # Get all cells surrounding the current cell, including already
        # occupied cells
        all_cells = grid.get_neighborhood(self.pos, True, True, 1)

        # Always give the option to not move
        free_cells = [self.pos]

        # Get rid of cells that we may not move to
        for x, y in all_cells:
            if grid.is_cell_empty((x, y)):
                free_cells.append((x, y))
            else:
                occupant = next(iter(grid[x][y]))

                if occupant.type not in no_overlap:
                    free_cells.append((x, y))

        return free_cells

    # Default move
    def move(self):
        grid = self.model.grid
        free_cells = self.get_moves()

        # Randomly select a new cell to move to
        new_cell = self.random.choice(free_cells)

        # Move the agent to the selected cell
        grid.move_agent(self, new_cell)


    def move_road(self):
        if self.on_road:
            # TODO:: check if transition move in one direction
            new_cell = (self.pos[0] + self.direction[0] * self.place.speed,
                       self.pos[1] + self.direction[1] * self.place.speed)

            if not self.model.map.get_place(new_cell):
                print("Off roading", self.pos, new_cell)
                exit(1)

            self.model.grid.move_agent(self, new_cell)

            # NOTE:: Can add multiple roads to make a curve add isinstance.
            if self.transition():
                # print("transistion to place")
                self.on_road = False

        else:
            # TODO:: check if transition else move normal
            # print("Place")
            self.move()

            if self.transition() and isinstance(self.place, Road):
                self.direction = self.place.flip(self.pos)
                self.on_road = True


    def step(self):
        if self.model.map.roads:
            self.move_road()
        else:
            self.move()

    def transition(self):
        """Check if the place the agent just moved to is a new place."""

        if not self.place.path.contains_point(self.pos):
            print("change")

        if not self.place.path.contains_point(self.pos):
            self.place = self.model.map.get_place(self.pos)

            return True

        return False
