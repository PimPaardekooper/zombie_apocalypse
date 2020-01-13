from .agent import Agent

class HumanAgent(Agent):
    def __init__(self, pos, model, fsm):
        super().__init__(pos, model, fsm)

        self.type = "human"
        self.traits['wants_to_bang'] = True
        self.states = [self.fsm.get_state("Idle")]


    def setVision(self, vision_radius):
        self.traits['vision'] = min(9, vision_radius)
