class State():
    """
    Determine whether a given agent may enter the current state, e.g. by
    evaluating the agent's traits.

    Args:
        agent (:obj:): The agent in the state.
    """
    def transition(self, agent):
        pass


    """
    Allows a state to not allow an agent to transtion to a new state.

    Args:
        agent (:obj:): The agent in the state.
    """
    def halt(self, agent):
        pass


    """
    Run a certain action when an agent transitions into the current state.

    Args:
        agent (:obj:): The agent in the state.
    """
    def on_enter(self, agent):
        pass


    """
    Run an action every tick of the model while an agent is in the current state.

    Args:
        agent (:obj:): The agent in the state.
    """
    def on_update(self, agent):
        pass


    """
    Run when an agent leaves a state.

    Args:
        agent (:obj:): The agent in the state.
    """
    def on_leave(self, agent):
        pass


    def __str__(self):
    """
    When trying to print a state, print its name.
    """
        return self.name
