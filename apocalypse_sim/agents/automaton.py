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
            state_name = state.name
            transitions = self.states[state_name]['transitions']

            new_states = []

            for transition in transitions:
                state_object = self.states[transition]['object']

                if state_object.transition(agent):
                    new_states.append(state_object)

            if new_states:
                state.on_leave(agent)
                agent.states.remove(state)

            for new_state in new_states:
                agent.states.append(new_state)
                new_state.on_enter(agent)
