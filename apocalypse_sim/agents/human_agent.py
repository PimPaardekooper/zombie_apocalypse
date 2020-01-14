from .agent import Agent

class HumanAgent(Agent):
    def __init__(self, pos, model, fsm, place):
        super().__init__(pos, model, fsm, place)

        self.type = "human"
        self.model.susceptible += 1


    def setVision(self, vision_radius):
        self.traits['vision'] = min(9, vision_radius)


    def __del__(self):
        print(self.model.susceptible)
        self.model.susceptible -= 1
        print(self.model.susceptible)
