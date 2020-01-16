class Automaton():
    def __init__(self):
        self.states = {}


    def add_state(self, state):
        if state.name not in self.states:
            self.states[state.name] = {
                "object": state,
                "transitions": []
            }


    def event(self, a, b):
        self.add_state(a)
        self.add_state(b)

        self.states[a.name]['transitions'].append(b.name)


    def set_initial_states(self, state_names, agent):
        agent.states = []

        for state_name in state_names:
            state = self.states[state_name]['object']

            agent.states.append(state)


    def update(self, agent):
        for state in agent.states.copy():

            # Make sure an agent is actually allowed
            # to leave a state.
            if state.halt(agent):
                continue

            # Get the string representation to use to easily
            # get corresponding transitions (our states
            # dictionary only uses strings for keys).
            state_name = state.name
            transitions = self.states[state_name]['transitions']

            new_states = []

            for transition in transitions:
                state_object = self.states[transition]['object']

                # Ask a state whether the given agent is allowed
                # to transition into it from the current state.
                if state_object.transition(agent):
                    new_states.append(state_object)

            # Only if new states to transition to were
            # found we will leave our current state
            if new_states:
                state.on_leave(agent)
                agent.states.remove(state)

            # We add the list of new states to our
            # active states list.
            for new_state in new_states:
                print("New state:", new_state)
                agent.states.append(new_state)
                new_state.on_enter(agent)
