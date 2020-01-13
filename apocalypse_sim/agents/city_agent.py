from .agent import Agent

class BuildingAgent(Agent):
    def __init__(self, pos, type, model, fsm):
        super().__init__(pos, model, fsm)

        self.type = type
