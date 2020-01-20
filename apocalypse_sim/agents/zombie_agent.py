from .agent import Agent

class ZombieAgent(Agent):
    def __init__(self, pos, model, fsm, place):
        super().__init__(pos, model, fsm, place)
        self.setVision(4)
        self.type = "zombie"
        self.model.infected += 1
        self.target = None

    def nearest_brain(self, neighbours):
        nearby_humans = [agent for agent in neighbours if agent.type == "human"]
        if len(nearby_humans) > 0:
            nearest = None
            for human in nearby_humans:
                distance = ((abs(human.pos[0] - self.pos[0])**2 + abs(human.pos[1] - self.pos[1])**2))**0.5
                if not nearest:
                    nearest = [distance, [human]]
                elif distance < nearest[0]:
                    nearest = [distance, [human]]
                elif distance == nearest[0]:
                    nearest[1].append(human)

            # If your target is not in list of nearest humans, pick a new
            # target
            if (not (self.target and self.target in nearest[1])):
                self.target = self.random.choice(nearest[1])

            return self.target.pos
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
