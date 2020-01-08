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
    else:
        portrayal = {"Shape": "circle", "r": 1, "Filled": "true", "Layer": 0,
                     "Text":  "(x, y)=" + str(agent.pos) + ", " +
                              "Type=" + agent.type
                     }

        if agent.type == "zombie":
            portrayal["Color"] = ["#FF0000", "#FF9999"]
            portrayal["stroke_color"] = "#00FF00"
        elif agent.type == "human":
            portrayal["Color"] = ["#0000FF", "#9999FF"]
            portrayal["stroke_color"] = "#000000"
        return portrayal

canvas_element = CanvasGrid(model_draw, 100, 100, 1000, 1000)
# happy_chart = ChartModule([{"Label": "happy", "Color": "Black"}])


# NOTE: Add sliders here
model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Agent density", 0.1, 0.01, 1.0, 0.01),
    "infected": UserSettableParameter("slider", "Amount infected", 0.1, 0.01, 1.0, 0.01)
}


server = ModularServer(Apocalypse,
                       [canvas_element],
                       "Apocalypse", model_params)
