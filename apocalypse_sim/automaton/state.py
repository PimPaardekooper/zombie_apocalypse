"""State class for a FSM. Each state should inherit from this class."""


class State():
    """Our own state class, used by the Finite State Machine."""

    def __init__(self):
        self.name = ""

    def transition(self, agent):
        """Check if an agent can transition into a state.

        Determine whether a given agent may enter the current state, e.g. by
        evaluating the agent's traits.

        Args:
            agent (:obj:): The agent in the state.

        """
        pass

    def halt(self, agent):
        """Allow a state to not allow an agent to transtion to a new state.

        Args:
            agent (:obj:): The agent in the state.

        """
        pass

    def on_enter(self, agent):
        """Run code when an agent transitions into the current state.

        Args:
            agent (:obj:): The agent in the state.

        """
        pass

    def on_update(self, agent):
        """Run code for every step.

        Run an action every tick of the model while an agent is in the
        current state.

        Args:
            agent (:obj:): The agent in the state.

        """
        pass

    def on_leave(self, agent):
        """Run when an agent leaves a state.

        Args:
            agent (:obj:): The agent in the state.

        """
        pass

    def __str__(self):
        """When trying to print a state, print its name."""
        return self.name

    def __eq__(self, other):
        """Object is equal if string is the same.

        Args:
            other (:obj:): The agent in the state.

        """
        return self.name == other
