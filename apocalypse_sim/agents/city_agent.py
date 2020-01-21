from .agent import Agent

class BuildingAgent(Agent):
    def __init__(self, pos, agent_type, model):
        super().__init__(pos, model)

        self.agent_type = agent_type
