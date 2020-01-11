from .agent import Agent

class HumanAgent(Agent):
    def __init__(self, pos, model, place):
        super().__init__(pos, model, place=place)

        self.type = "human"


    def setVision(self, visionRadius):
        self.traits.vision = max(9, visionRadius)
