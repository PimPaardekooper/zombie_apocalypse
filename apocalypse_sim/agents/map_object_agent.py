from mesa import Agent as MesaAgent

class MapObjectAgent(MesaAgent):
    def __init__(self, pos, agent_type, model):
        super().__init__(pos, model)

        self.type = agent_type
