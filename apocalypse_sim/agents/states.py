from .state import State

class Idle(State):
    def __init__(self):
        self.name = "Idle"

    # Function that determines if another state may transition
    # into the current state.
    def transition(self, agent):
        return True


    def on_enter(self, agent):
        print("Entered Idle state")

        pass


    def on_update(self, agent):
        print(agent.pos)

        pass


    def on_leave(self, agent):
        print("Left Idle state")

        pass


class Tracking(State):
    def __init__(self):
        self.name = "Tracking"
