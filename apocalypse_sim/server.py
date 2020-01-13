"""server.py

Visualize the current state, says what each object looks like given there
attributes and makes slider so you can change the model.
"""
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter

import os
import webbrowser
import tornado.ioloop

from model import Apocalypse

class ModularServerExtd(ModularServer):

    def __init__(self, model_cls, visualization_elements, name="Mesa Model",
                 model_params={}):
        super().__init__(model_cls, visualization_elements, name, model_params)

    def launch(self, port=None):

        """ Run the app. """
        if port is not None:
            self.port = port
        url = 'http://127.0.0.1:{PORT}'.format(PORT=self.port)
        print('Interface starting at {url}'.format(url=url))
        self.listen(self.port)

        if os.getenv('WEBBY', "0") == "0":
            webbrowser.open(url)

        os.environ["WEBBY"] = "1"

        tornado.autoreload.start()
        tornado.ioloop.IOLoop.current().start()

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
        portrayal["Color"] = ["#dd42f5"]
    elif agent.type == "road":
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#f5e3427A"]
    else:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#000000"]

    return portrayal

grid_height = 10
grid_width = 10
canvas_height = 600
canvas_width = canvas_height

canvas_element = CanvasGrid(model_draw, grid_height, grid_width, canvas_height, canvas_width)

# happy_chart = ChartModule([{"Label": "happy", "Color": "Black"}])


# NOTE: Add sliders here
model_params = {
    "height": grid_height,
    "width": grid_width,
    "density": UserSettableParameter("slider", "Agent density", 0.1, 0.01, 1.0, 0.01),
    "infection_change": UserSettableParameter("slider", "Change getting infected", 0.1, 0.01, 1.0, 0.01),
    "map_id": UserSettableParameter("slider", "Map id (max 4)", value=0, min_value=0, max_value=4, step=1, choices=[0,1,2,3,4])
}

chart = ChartModule([{"Label": "susceptible",
                      "Color": "Green"},
                      {"Label": "infected",
                      "Color": "Red"}],
                    data_collector_name='datacollector')

server = ModularServerExtd(Apocalypse,
                       [canvas_element, chart],
                       "Apocalypse", model_params)
