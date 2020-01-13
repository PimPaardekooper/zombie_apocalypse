from .agent import Agent

class HumanAgent(Agent):
    def __init__(self, pos, model, fsm, place):
        super().__init__(pos, model, fsm, place)

        self.type = "human"
        self.states = [fsm.get_state("Idle")]


    def setVision(self, vision_radius):
        self.traits['vision'] = min(9, vision_radius)
