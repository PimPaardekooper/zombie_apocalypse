"""Agent portrayal.

Visualize the current state and says what each object looks like given there
attribute.
"""
import os


def model_draw(agent):
    """Portrayal Method for canvas.

    Gives the agent the shapes and colors and makes the text you get when
    hovering over an agent.
    """
    if agent is None:
        return

    portrayal = {
        "Shape": "circle",
        "r": 1,
        "Filled": "true",
        "Layer": 1
    }

    if agent.agent_type == "zombie":
        portrayal = zombie_portrayal(agent, portrayal)
    elif agent.agent_type == "human":
        portrayal = human_portrayal(agent, portrayal)
    elif agent.agent_type == "city":
        portrayal = city_portrayal(agent, portrayal)
    elif agent.agent_type == "road":
        portrayal = road_portrayal(agent, portrayal)
    else:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true",
                     "Layer": 0, "Text": "pos:" + str(agent.pos)}
        portrayal["Color"] = ["#000000"]

    return portrayal


def zombie_portrayal(agent, portrayal):
    """Portrayal zombie agent."""
    agent_properties = {}

    agent_properties["Pos"] = "(x, y) =" + str(agent.pos)
    agent_properties["Type"] = agent.agent_type
    agent_properties["States"] = str([x.name for x in agent.states])
    agent_properties["Identifier"] = str(agent.unique_id)

    portrayal["Color"] = ["#A41E1F", "#DE6C6B"]
    portrayal["stroke_color"] = "#A41E1F"

    return {**portrayal, **agent_properties}


def human_portrayal(agent, portrayal):
    """Portrayal human agent."""
    agent_properties = {}

    agent_properties["Pos"] = "(x, y) =" + str(agent.pos)
    agent_properties["Type"] = agent.agent_type
    agent_properties["States"] = str([x.name for x in agent.states])
    agent_properties["Identifier"] = str(agent.unique_id)

    if "zombie_kills" in agent.traits:
        agent_properties["Kills"] = str(agent.traits["zombie_kills"])
    else:
        agent_properties["Kills"] = "0"

    agent_properties["Direction"] = str(agent.direction)

    if "infected" in agent.traits:
        portrayal["Color"] = ["#80C904", "#4D7902"]
    else:
        portrayal["Color"] = ["#0000FF", "#9999FF"]
    
    if os.environ["mode"] == "5" and agent.pos == (4,4):
        # Set color green in situations.
        portrayal["Color"] = ["#03fc77", "#9999FF"]

    portrayal["stroke_color"] = "#000000"

    return {**portrayal, **agent_properties}


def road_portrayal(agent, portrayal):
    """Portrayal road agent."""
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    portrayal["Color"] = ["#f5e3427A"]

    return portrayal


def city_portrayal(agent, portrayal):
    """Portrayal city agent."""
    portrayal = {"Shape": "rect", "w": 1,
                 "h": 1, "Filled": "true", "Layer": 0}

    if agent.color != "":
        portrayal["Color"] = agent.color + "40"
    else:
        portrayal["Color"] = ["#dd42f540"]

    return portrayal
