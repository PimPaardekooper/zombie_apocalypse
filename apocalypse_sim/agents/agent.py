from mesa import Model
from mesa import Agent as MesaAgent

class Agent(MesaAgent):
    def __init__(self, pos, model):
        super().__init__(pos, model)

        self.pos = pos
        self.traits = {}


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


    def step(self):
        self.move()

    def transition(self, new_pos):
        """Transition to new place if new position is not in the same place."""
        if not self.traits["place"].contains_point(new_pos):
            self.traits.place = self.model.get_place(new_pos)
            # TODO:: change agents attributes given the new place.
