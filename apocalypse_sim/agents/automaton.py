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

            # state.on_enter(agent)
            agent.states.append(state)


    def update(self, agent):
        fr = agent.states.copy()

        for state in fr:
            
            state_name = state.name
            # print("\n\n", "State_name:  ", state_name, "\n\n")
            transitions = self.states[state_name]['transitions']

            new_states = []

            # if state_name == "Infect":
            #     print("I'm infected")

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

            if len(new_states) == 2:
                print("Came from", state.name, "New states:", [x.name for x in new_states])
