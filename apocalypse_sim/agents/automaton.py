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


    def get_state(self, state_name):
        if state_name in self.states:
            return self.states[state_name]['object']

        raise ValueError("State does not exist")


    def transition(self, agent):
        for state in agent.states:
            state_name = state.name
            transitions = self.states[state_name]['transitions']

            for transition in transitions:
                state_object = self.states[transition]['object']

                if state_object.transition(agent):
                    state.on_leave(agent)

                    agent.states.remove(state)
                    agent.states.append(state_object)

                    state_object.on_enter(agent)
