from .state import State
from .human_agent import HumanAgent
from .zombie_agent import ZombieAgent

class Idle(State):
    def __init__(self):
        self.name = "Idle"

    # Function that determines if another state may transition
    # into the current state.
    def transition(self, agent):
        return agent.traits["desire"] == 0


    def on_enter(self, agent):
        if agent.pos[1] > 0:
            agent.traits["desire"] = 1
        else:
            agent.traits["desire"] = 0


    def on_update(self, agent):
        agent.move()

        agent.traits["desire"] += 1


    def on_leave(self, agent):
        print("Left Idle state")

        pass


class Reproduce(State):
    def reproduce(self, agent):
        neighbors = agent.model.grid.get_neighbors(agent.pos, moore=False)

        for neighbour in neighbors:
            if neighbour.type != "human":
                return False

            desire = neighbour.traits["desire"]

            if desire and desire > 2:
                birth_cells = agent.get_moves()

                if not birth_cells:
                    birth_cells = neighbour.get_moves()

                new_cell = agent.random.choice(birth_cells)

                new_agent = HumanAgent(new_cell, agent.model, agent.fsm, {})

                agent.model.grid.place_agent(new_agent, new_cell)
                agent.model.schedule.add(new_agent)

                return neighbour

        return False


    def __init__(self):
        self.name = "Reproduce"


    def transition(self, agent):
        if agent.traits["desire"] > 2:
            return True


    def on_enter(self, agent):
        mate = self.reproduce(agent)

        if mate:
            agent.traits["desire"] = 0
            mate.traits["desire"] = 0


    def on_update(self, agent):
        mate = self.reproduce(agent)

        if mate:
            agent.traits["desire"] = 0
            mate.traits["desire"] = 0

        agent.move()


    def on_leave(self, agent):
        pass


class Wandering(State):
    def __init__(self):
        self.name = "Wandering"


    def transition(self, agent):
        return True


    def on_update(self, agent):
        agent.move()


class ChasingHuman(State):
    def __init__(self):
        self.name = "ChasingHuman"


    def transition(self, agent):
        neighbours = agent.model.grid.get_neighbors(agent.pos, True, True, agent.traits["vision"])
        nearest_human = agent.nearest_brain(neighbours)


class Infect(State):
    def __init__(self):
        self.name = "Infect"


    def transition(self, agent):
        if agent.type != "zombie":
            return False

        neighbors = agent.model.grid.get_neighbors(agent.pos, moore=False)

        for neighbour in neighbors:
            if neighbour.type == "human":
                self.target = neighbour

                return True

        return False


    def on_enter(self, agent):
        pos = self.target.pos
        grid = agent.model.grid
        fsm = self.target.fsm
        schedule = self.target.model.schedule

        zombie = ZombieAgent(pos, agent.model, fsm, {})

        fsm.set_initial_states(["Wandering"], zombie)

        grid.remove_agent(self.target)
        schedule.remove(self.target)

        del self.target

        grid.place_agent(zombie, pos)
        schedule.add(zombie)
