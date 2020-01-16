from .agent import Agent

class ZombieAgent(Agent):
    def __init__(self, pos, model, fsm, place):
        super().__init__(pos, model, fsm, place)
        self.setVision(4)
        self.type = "zombie"
        self.model.infected += 1

    def nearest_brain(self, neighbours):
        nearby_brains = []

        for neighbour in neighbours:
            if not neighbour.type == "human":
                continue

            if "Infected" not in [state.name for state in neighbour.states]:
                nearby_brains.append(neighbour.pos)


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
        neighbours = self.model.grid.get_neighbors(self.pos, True, True, self.traits["vision"])
        nearest_human = self.nearest_brain(neighbours)

        if nearest_human:
            new_cell = self.best_cell([nearest_human[0], nearest_human[1]])
        else:
            # Randomly select a new cell to move to
            new_cell = self.random.choice(self.get_moves())

        # Move the agent to the selected cell
        self.model.grid.move_agent(self, new_cell)


    def setVision(self, visionRadius):
        self.traits["vision"] = min(9, visionRadius)


    def __del__(self):
        self.model.infected -= 1
