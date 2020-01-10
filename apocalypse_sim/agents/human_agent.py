from agent import Agent

class HumanAgent(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)

        self.type = "human"


    def setVision(self, visionRadius):
        self.traits.vision = max(9, visionRadius);
