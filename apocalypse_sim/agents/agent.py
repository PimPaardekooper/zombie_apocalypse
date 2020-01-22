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
        self.time_alive = 0

        self.agent_type = ""

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
        all_cells = self.neighbors()

        # Always give the option to not move
        free_cells = [self.pos]

        # Get rid of cells that we may not move to
        for cell in all_cells:
            x, y = cell.pos

            if grid.is_cell_empty((x, y)):
                free_cells.append((x, y))
            else:
                panzerkampfwagen = False

                for cell in grid[x][y]:
                    if cell.agent_type in no_overlap:
                        panzerkampfwagen = True

                        break

                if not panzerkampfwagen:
                    free_cells.append((x, y))

        return free_cells


    # Gets the nearest available cell of a coordinate
    def best_cell(self, coord):
        if coord[0] == self.pos[0] and coord[1] == self.pos[1]:
            return self.pos

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
        self.model.grid.remove_agent(self)
        self.model.schedule.remove(self)

        if self.agent_type == "zombie":
            self.model.infected -= 1
        elif self.agent_type == "human":
            self.model.susceptible -= 1

        del self


    def neighbors(self, moore=True, include_center=True, radius=1):
        return self.model.grid.get_neighbors(self.pos, moore, include_center, radius)


    def step(self):
        self.time_alive += 1

        self.fsm.update(self)

        for state in self.states:
            if not self.pos:
                continue

            state.on_update(self)
