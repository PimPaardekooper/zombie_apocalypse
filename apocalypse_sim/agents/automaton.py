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

            state.on_enter(agent)
            agent.states.append(state)


    def update(self, agent):
        for state in agent.states.copy():
            state_name = state.name
            transitions = self.states[state_name]['transitions']

            for transition in transitions:
                state_object = self.states[transition]['object']

                if state_object.transition(agent):
                    state.on_leave(agent)

                    agent.states.remove(state)
                    agent.states.append(state_object)

                    state_object.on_enter(agent)
