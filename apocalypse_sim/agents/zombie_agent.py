from .agent import Agent

class ZombieAgent(Agent):
    def __init__(self, pos, model, place):
        super().__init__(pos, model, place=place)

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

    # def move():
    #
    #     free_cells = self.get_moves()
    #
    #     # tasty_brain = self.nearest_brain(neighbours)
    #
    #     # Randomly select a new cell to move to
    #     new_cell = self.random.choice(free_cells)
    #
    #     # Move the agent to the selected cell
    #     grid.move_agent(self, new_cell)


    def setVision(self, visionRadius):
        self.traits.vision = max(9, visionRadius)
