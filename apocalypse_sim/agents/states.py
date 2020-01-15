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


    def random_move(self, agent):
        free_cells = agent.get_moves()
        new_cell = agent.random.choice(free_cells)

        agent.model.grid.move_agent(agent, new_cell)


    def transition(self, agent):
        f = [x.name for x in agent.states]

        if "Infect" in f:
            print("Transitioning from Infect")

        neighbours = agent.model.grid.get_neighbors(agent.pos, True, True, agent.traits["vision"])

        if agent.type == "zombie":
            x = not agent.nearest_brain(neighbours)
            # print(agent.id, "wants to transition to wandering from", agent.states, x)
            return x


        return not agent.find_escape(neighbours)


    def on_enter(self, agent):
        # print("Just wandering about")

        self.random_move(agent)


    def on_update(self, agent):
        self.random_move(agent)


class AvoidingZombie(State):
    def __init__(self):
        self.name = "AvoidingZombie"


    def get_best_cell(self, agent):
        neighbours = agent.model.grid.get_neighbors(agent.pos, True, True, agent.traits["vision"])
        direction = agent.find_escape(neighbours)

        if direction:
            # Calculate the coordinate the agent wants to move to
            new_x = agent.pos[0] + direction[0]
            new_y = agent.pos[1] + direction[1]

            return agent.best_cell([new_x, new_y])

        return None


    def transition(self, agent):
        return agent.type == "human" and self.get_best_cell(agent)


    def on_enter(self, agent):
        best_cell = self.get_best_cell(agent)

        agent.model.grid.move_agent(agent, best_cell)


    def on_update(self, agent):
        best_cell = self.get_best_cell(agent)

        if best_cell:
            agent.model.grid.move_agent(agent, best_cell)


class ChasingHuman(State):
    def __init__(self):
        self.name = "ChasingHuman"


    def get_best_cell(self, agent):
        neighbours = agent.model.grid.get_neighbors(agent.pos, True, True, agent.traits["vision"])
        nearest_human = agent.nearest_brain(neighbours)

        if nearest_human:
            return agent.best_cell([nearest_human[0], nearest_human[1]])

        return None


    def transition(self, agent):
        if agent.type != "zombie":
            return False

        human = self.get_best_cell(agent)

        if not human:
            return False
            
        self_x = agent.pos[0]
        self_y = agent.pos[1]
        human_x = human[0]
        human_y = human[1]

        if ((abs(self_x - human_x) == 1 and abs(self_y - human_y) == 0) or
           (abs(self_y - human_y) == 1 and abs(self_x - human_x) == 0)):
            return True

        return False



    def on_enter(self, agent):
        # print("Mon wants to go again")
        best_cell = self.get_best_cell(agent)

        agent.model.grid.move_agent(agent, best_cell)


    def on_update(self, agent):
        best_cell = self.get_best_cell(agent)

        if best_cell:
            agent.model.grid.move_agent(agent, best_cell)


    # def on_leave(self, agent):
    #     print(agent.id, "leaving ChasingHuman")


class Infect(State):
    def __init__(self):
        self.name = "Infect"


    def transition(self, agent):
        if agent.type != "zombie":
            return False

        neighbors = agent.model.grid.get_neighbors(agent.pos, moore=False)

        for neighbour in neighbors:
            if neighbour.type == "human":

                # print(agent.id, "About to transition into Infect")

                self.target = neighbour

                # print(agent.id, "targets", self.target.id)

                return True

        return False


    def on_enter(self, agent):
        # print("Infecting")

        pos = self.target.pos
        grid = agent.model.grid
        fsm = self.target.fsm
        schedule = self.target.model.schedule

        zombie = ZombieAgent(pos, agent.model, fsm, {})

        fsm.set_initial_states(["Wandering"], zombie)

        # print("'Deleted target'", self.target.pos)

        grid.remove_agent(self.target)
        schedule.remove(self.target)

        # zombie.id = zombie.model.random.randint(0, 1000)

        del self.target

        grid.place_agent(zombie, pos)
        schedule.add(zombie)


    # def on_leave(self, agent):
    #     print("left infection")
