class State():
    """
    Determine whether a given agent may enter
    the current state, e.g. by evaluating the
    agent's traits.
    """
    def transition(self, agent):
        pass


    """
    Run a certain action when an agent transitions
    into the current state.
    """
    def on_enter(self, agent):
        pass


    """
    Run an action every tick of the model while an
    agent is in the current state.
    """
    def on_update(self, agent):
        pass


    """
    Run when an agent leaves a state.
    """
    def on_leave(self, agent):
        pass


    def __str__(self):
        return self.name
