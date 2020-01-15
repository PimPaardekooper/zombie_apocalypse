from mesa import Model
from mesa import Agent as MesaAgent

from .map_object import Road

from shapely.geometry import Point

class Agent(MesaAgent):
    def __init__(self, pos, model, fsm, place):
        super().__init__(model.total, model)

        self.states = []
        self.traits = {}
        self.fsm = fsm
        self.pos = pos

        self.model = model
        self.model.total += 1

        self.place = place
        self.direction = (0, 0)
        self.on_road = False

    def get_moves(self):
        grid = self.model.grid
        no_overlap = ["wall", "human", "zombie"]

        # Get all cells surrounding the current cell, including already
        # occupied cells
        all_cells = grid.get_neighborhood(self.pos, False, False, 1)

        # Always give the option to not move
        free_cells = [self.pos]

        # Get rid of cells that we may not move to
        for x, y in all_cells:

            if grid.is_cell_empty((x, y)):
                free_cells.append((x, y))
            else:
                panzerkampfwagen = False

                for cell in grid[x][y]:
                    if cell.type in no_overlap:
                        panzerkampfwagen = True

                        break

                if not panzerkampfwagen:
                    free_cells.append((x, y))

        return free_cells

    # Gets the nearest available cell of a coordinate
    def best_cell(self, coord):
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

    # # Default move
    # def move(self):
    #     grid = self.model.grid
    #     free_cells = self.get_moves()
    #
    #     # Randomly select a new cell to move to
    #     new_cell = self.random.choice(free_cells)
    #
    #     print("Old pos:", self.pos, "Available:", free_cells, "Chose cell:", new_cell)
    #
    #     # Move the agent to the selected cell
    #     grid.move_agent(self, new_cell)


    # # def move_road(self):
    # #     if self.on_road:
    # #         # TODO:: check if transition move in one direction
    # #         new_cell = (self.pos[0] + self.direction[0] * self.place.speed,
    # #                    self.pos[1] + self.direction[1] * self.place.speed)
    # #
    # #         if not self.model.map.get_place(new_cell):
    # #             print("Off roading", self.pos, new_cell)
    # #             exit(1)
    # #
    # #         self.model.grid.move_agent(self, new_cell)
    # #
    # #         # NOTE:: Can add multiple roads to make a curve add isinstance.
    # #         if self.transition():
    # #             # print("transistion to place")
    # #             self.on_road = False
    # #
    # #     else:
    # #         # TODO:: check if transition else move normal
    # #         # print("Place")
    # #         self.move()
    # #
    # #         if self.transition() and isinstance(self.place, Road):
    # #             self.direction = self.place.flip(self.pos)
    # #             self.on_road = True
    # #
    # #
    def step(self):
        if self in self.model.locked:
            return

        # if self.model.map.roads:
        #     self.move_road()
        # else:
        # print("Called", self.id, "'s FSM update")
        self.fsm.update(self)

        for state in self.states:
            # print("Running on_update of", state.name, "on", self.id)
            state.on_update(self)


    # def transition(self):
    #     """Check if the place the agent just moved to is a new place."""
    #     if not self.place.poly.intersects(Point(self.pos)):
    #         self.place = self.model.map.get_place(self.pos)
    #
    #         return True
    #
    #     return False
