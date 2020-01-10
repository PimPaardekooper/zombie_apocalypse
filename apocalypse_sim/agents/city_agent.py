from agent import Agent

class BuildingAgent(Agent):
    def __init__(self, pos, type, model):
        super().__init__(pos, model)

        self.type = type
