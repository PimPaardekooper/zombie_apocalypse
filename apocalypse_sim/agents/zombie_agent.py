from .agent import Agent

class ZombieAgent(Agent):
    def __init__(self, pos, model, fsm, place):
        super().__init__(pos, model, fsm, place)
        self.setVision(4)
        self.type = "zombie"

    def nearest_brain(self, neighbours):
        nearby_brains = [brain.pos for brain in neighbours if brain.type == "human"]
        if len(nearby_brains) > 0:
            nearest = 0
            for brain in nearby_brains:
                distance = (abs(brain[0] - self.pos[0])**2 + abs(brain[1] - self.pos[1])**2)**0.5
                if nearest == 0 or nearest < distance:
                    nearest = distance
                    nearest_x = brain[0]
                    nearest_y = brain[1]
            return (nearest_x, nearest_y)
        return None

    def move(self):
        grid = self.model.grid
        free_cells = self.get_moves()

        neighbours = self.model.grid.get_neighbors(self.pos, True, True, self.traits["vision"])

        tasty_brain = self.nearest_brain(neighbours)
        # print(str(self.pos) + "has nearest brain " + str(tasty_brain))

        if tasty_brain:
            smol_d = float("Inf")
            for cell in free_cells:
                d_x = abs(tasty_brain[0] - cell[0])
                d_y = abs(tasty_brain[1] - cell[1])
                d = (d_x**2 + d_y**2)**0.5
                if d < smol_d:
                    smol_d = d
                    new_cell = cell
        else:
            # Randomly select a new cell to move to
            new_cell = self.random.choice(free_cells)
        # Move the agent to the selected cell
        grid.move_agent(self, new_cell)
        # print("moved to " + str(new_cell))


    def setVision(self, visionRadius):
<<<<<<< HEAD
        self.traits['vision'] = min(9, visionRadius);
=======
        self.traits["vision"] = min(9, visionRadius)
>>>>>>> master
