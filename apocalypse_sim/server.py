"""server.py

Visualize the current state, says what each object looks like given there
attributes and makes slider so you can change the model.
"""
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

from model import Apocalypse

def model_draw(agent):
    '''
    Portrayal Method for canvas
    '''
    if agent is None:
        return

    portrayal = {"Shape": "circle", "r": 1, "Filled": "true", "Layer": 1,
                 "Text": "(x, y)=" + str(agent.pos)}

    if agent.type == "zombie":
        portrayal["Text"] = "(x, y)=" + str(agent.pos) + ", Type=" + agent.type \
                                      + ", Place=" + str(agent.place)

        portrayal["Color"] = ["#FF0000", "#FF9999"]
        portrayal["stroke_color"] = "#00FF00"
    elif agent.type == "human":
        portrayal["Text"] = "(x, y)=" + str(agent.pos) + ", Type=" + agent.type \
                                      + ", Place=" + str(agent.place)
        portrayal["Color"] = ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"
    elif agent.type == "city":
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#dd42f540"]
    elif agent.type == "road":
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#f5e3427A"]
    else:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#000000"]

    return portrayal

grid_height = 100
grid_width = 100
canvas_height = 600
canvas_width = canvas_height

canvas_element = CanvasGrid(model_draw, grid_height, grid_width, canvas_height, canvas_width)

# happy_chart = ChartModule([{"Label": "happy", "Color": "Black"}])


# NOTE: Add sliders here
model_params = {
    "height": grid_height,
    "width": grid_width,
    "density": UserSettableParameter("slider", "Agent density", 0.05, 0.01, 1.0, 0.01),
    "infection_change": UserSettableParameter("slider", "Change getting infected", 0.1, 0.01, 1.0, 0.01),
    "map_id": UserSettableParameter("slider", "Map id (max 4)", value=0, min_value=0, max_value=4, step=1, choices=[0,1,2,3,4])
}

chart = ChartModule([{"Label": "susceptible",
                      "Color": "Green"},
                      {"Label": "infected",
                      "Color": "Red"}],
                    data_collector_name='datacollector')

server = ModularServer(Apocalypse,
                       [canvas_element, chart],
                       "Apocalypse", model_params)
