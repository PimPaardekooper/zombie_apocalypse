from automaton.states import *
import os


class Automaton():
    """Our automaton class. This is used to program finite state machines
    (FSM).

    """

    def __init__(self, model):
        """Initialize the FSM and program it.

        Args:
            (:obj:) model: Model object the FSM belongs to.

        """
        self.states = {}

        # Zombie movement
        self.event(ZombieWandering(), ChasingHuman())
        self.event(ChasingHuman(), ZombieWandering())

        # Zombie human interaction
        self.event(Idle(), InteractionHuman())
        self.event(InteractionHuman(), InfectHuman())
        self.event(InteractionHuman(), RemoveZombie())
        self.event(InfectHuman(), Idle())

        # Human movement
        self.event(HumanWandering(), AvoidingZombie())
        self.event(AvoidingZombie(), HumanWandering())

        if model.grouping:
            self.event(HumanWandering(), FormingHerd())
            self.event(AvoidingZombie(), FormingHerd())
            self.event(FormingHerd(), HumanWandering())
            self.event(FormingHerd(), AvoidingZombie())

        # Human health
        self.event(Susceptible(), Infected())
        self.event(Infected(), Turned())

        # Through doorway
        if os.environ["mode"] == "4":
            self.event(FindDoor(), Escaped())
        elif os.environ["mode"] == "5":
            self.event(HumanWandering(), OnRoad())
            self.event(FormingHerd(), OnRoad())
            self.event(AvoidingZombie(), OnRoad())
            self.event(ZombieWandering(), OnRoad())

            self.event(OnRoad(), HumanWandering())
            self.event(OnRoad(), FormingHerd())
            self.event(OnRoad(), AvoidingZombie())
            self.event(OnRoad(), ZombieWandering())

    def add_state(self, state):
        """Adds a state to the Automaton.

        Args:
            state (:obj:): the state to be added to the automaton.

        """
        if state.name not in self.states:
            self.states[state.name] = {
                "object": state,
                "transitions": []
            }

    def event(self, a, b):
        """Add a transition from state a to state b to the automaton.

        Args:
            a (:obj:): the state to transition from.
            b (:obj:): the state to transition to.
        """
        self.add_state(a)
        self.add_state(b)
        self.states[a.name]['transitions'].append(b.name)

    def set_initial_states(self, state_names, agent):
        """Set the states an agent has to be initialized with.

        Args:
            state_names (string): The string names referring to state objects.
            agent (:obj:): Agent whomst'd've initial states have to be set.
        """
        agent.states = []

        for state_name in state_names:
            state = self.states[state_name]['object']
            agent.states.append(state)

    def switch_to_state(self, agent, old, new):
        """Force a state-switch before the Automaton's update function
        is called. This is riskier than using the Automaton's own update
        function since no verification is made to ensure proper transitions.

        Args:
            agent (:obj:): Agent whomst'd've state has to be switched.
            old (string): String referring to the state we want to
                          transition from.
            new (string): String referring to the state we want to
                          transition to.
        """
        if new in self.states[old]["transitions"]:
            old_state_obj = self.states[old]["object"]
            new_state_obj = self.states[new]["object"]

            agent.states.remove(old_state_obj)
            old_state_obj.on_leave(agent)

            agent.states.append(new_state_obj)
            new_state_obj.on_enter(agent)

    def update(self, agent):
        """Allow agent to possibly transition from current state to a
        registered and verified new state.

        Args:
            agent (:obj:): Agent whomst'd've states can be updated.

        """
        for state in agent.states.copy():
            if not agent.pos:
                continue

            if state.halt(agent):
                continue

            # Use string representation for easy state lookup.
            state_name = state.name
            transitions = self.states[state_name]['transitions']

            new_states = []

            for transition in transitions:
                if not agent.pos:
                    continue

                state_object = self.states[transition]['object']

                # Ask a state whether the given agent is allowed
                # to transition into it from the current state.
                if state_object.transition(agent):
                    new_states.append(state_object)

            if new_states:
                state.on_leave(agent)
                agent.states.remove(state)

            # We add the list of new states to our
            # active states list.
            # If transition to road don't transition to other states.
            if OnRoad() in new_states:
                for new_state in new_states:
                    if new_state == "OnRoad":
                        agent.states.append(new_state)
                        new_state.on_enter(agent)
            else:
                for new_state in new_states:
                    agent.states.append(new_state)
                    new_state.on_enter(agent)
