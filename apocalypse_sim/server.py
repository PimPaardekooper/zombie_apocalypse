"""server.py

Visualize the current state, says what each object looks like given there
attributes and makes slider so you can change the model.
"""
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from CSSImportModule import CSSImportModule

import os
import webbrowser
import tornado.ioloop
import numpy as np

import random
import sys

from model import Apocalypse


class ModularServerExtd(ModularServer):
    def __init__(self, model_cls, visualization_elements, name="Mesa Model",
                 model_params={}):

        self.verbose = False

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

    agent_properties = {}

    portrayal = {
        "Shape": "circle",
        "r": 1,
        "Filled": "true",
        "Layer": 1
    }

    if agent.agent_type == "zombie":
        agent_properties["Pos"] = "(x, y) =" + str(agent.pos)
        agent_properties["Type"] = agent.agent_type
        agent_properties["States"] = str([x.name for x in agent.states])
        agent_properties["Identifier"] = str(agent.unique_id)

        portrayal["Color"] = ["#A41E1F", "#DE6C6B"]
        portrayal["stroke_color"] = "#A41E1F"

        portrayal = {**portrayal, **agent_properties}
    elif agent.agent_type == "human":
        agent_properties["Pos"] = "(x, y) =" + str(agent.pos)
        agent_properties["Type"] = agent.agent_type
        agent_properties["States"] = str([x.name for x in agent.states])
        agent_properties["Identifier"] = str(agent.unique_id)
        agent_properties["Kills"] = str(agent.traits["zombie_kills"]) if "zombie_kills" in agent.traits else "0"
        agent_properties["Direction"] = str(agent.direction)

        portrayal["Color"] = ["#80C904", "#4D7902"] if "infected" in agent.traits else ["#0000FF", "#9999FF"]
        portrayal["stroke_color"] = "#000000"

        portrayal = {**portrayal, **agent_properties}
    elif agent.agent_type == "city":
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}

        if agent.color != "":
            portrayal["Color"] = agent.color + "40"
        else:
            portrayal["Color"] = ["#dd42f540"]
    elif agent.agent_type == "road":
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#f5e3427A"]
    else:
        portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
        portrayal["Color"] = ["#000000"]

    return portrayal

seed = random.randrange(sys.maxsize)
patient_zero = False

provinces = ["Groningen", "Friesland", "Drenthe", "Overijssel", "Flevoland",
            "Gelderland", "Utrecht", "Noord-Holland", "Zuid-Holland", "Zeeland",
            "Noord-Brabant", "Limburg", "---"]

if os.environ["mode"] == "1":
    # Test modes
    grid_height = 10
    grid_width = 10
    map_id = 4
    canvas_height = 1000
    canvas_width = canvas_height
    kill_chance = 0

    model_params = {
        "height": grid_height,
        "width": grid_width,
        "seed": UserSettableParameter("number", "seed", value=str(seed)),
        "map_id": UserSettableParameter("slider", "Map id (max 4)", value=map_id, min_value=0, max_value=4, step=1),
        "human_kill_agent_chance": UserSettableParameter("slider", "Human kill chance", value=kill_chance, min_value=0, max_value=1, step=0.01),
        "grouping": UserSettableParameter("checkbox", "Grouping", value=True),
        "human_vision": UserSettableParameter("slider", "Human vision", value=4, min_value=1, max_value=8, step=1),
    }
elif os.environ["mode"] == "2":
    # Netherlands
    grid_height = 200
    grid_width = 200
    map_id = 0
    canvas_height = 1000
    canvas_width = canvas_height
    patient_zero = False
    kill_chance = 0
    grouping = False
    density = 0.5

    # NOTE: Add sliders here
    model_params = {
        "height": grid_height,
        "width": grid_width,
        "seed": UserSettableParameter("number", "seed", value=str(seed)),
        "density": UserSettableParameter("slider", "Agent density", value=density, min_value=0.01, max_value=1.0, step=0.01),
        "infected_chance": UserSettableParameter("slider", "Change getting infected", value=0.1, min_value=0.01, max_value=1.0, step=0.01),
        "human_kill_agent_chance": UserSettableParameter("slider", "Human kill chance", value=kill_chance, min_value=0, max_value=1, step=0.01),
        "map_id": map_id,
        # "city_id":  UserSettableParameter("slider", "City id (max 4)", value=0, min_value=0, max_value=8, step=1),
        "province":  UserSettableParameter("choice", "Province outbreak", "Noord-Holland", choices=provinces),
        "patient_zero": UserSettableParameter("checkbox", "Patient zero", value=patient_zero),
        "grouping": UserSettableParameter("checkbox", "Grouping", value=grouping),
        "human_vision": UserSettableParameter("slider", "Human vision", value=4, min_value=1, max_value=8, step=1),
        "zombie_vision": UserSettableParameter("slider", "Zombie vision", value=7, min_value=1, max_value=8, step=1),
    }
else:
    map_id = 0
    grid_height = 50
    grid_width = 50
    canvas_height = 1000
    canvas_width = canvas_height


    model_params = {
        "height": grid_height,
        "width": grid_width,
        "seed": UserSettableParameter("number", "seed", value=str(seed)),
        "density": UserSettableParameter("slider", "Agent density", value=0.2, min_value=0.01, max_value=1.0, step=0.01),
        "infected_chance": UserSettableParameter("slider", "Change getting infected", value=0.1, min_value=0.01, max_value=1.0, step=0.01),
        "human_kill_agent_chance": UserSettableParameter("slider", "Human kill chance", value=0.3, min_value=0, max_value=1, step=0.01),
        "map_id": UserSettableParameter("slider", "Map id (max 4)", value=map_id, min_value=0, max_value=7, step=1),
        "city_id":  UserSettableParameter("slider", "City id (max 4)", value=0, min_value=0, max_value=8, step=1),
        "province":  UserSettableParameter("choice", "Province outbreak", "", choices=provinces),
        "patient_zero": UserSettableParameter("checkbox", "Patient zero", value=patient_zero),
        "grouping": UserSettableParameter("checkbox", "Grouping", value=True),
        "human_vision": UserSettableParameter("slider", "Human vision", value=4, min_value=1, max_value=8, step=1),
        "zombie_vision": UserSettableParameter("slider", "Zombie vision", value=7, min_value=1, max_value=8, step=1),
    }

canvas_element = CanvasGrid(model_draw, grid_height, grid_width, canvas_height, canvas_width)

chart = ChartModule([{"Label": "susceptible",
                      "Color": "Green"},
                      {"Label": "infected",
                      "Color": "Red"},
                      {"Label": "recovered",
                      "Color": "Black"}],
                    data_collector_name='datacollector')

custom_styling = CSSImportModule()

server = ModularServerExtd(Apocalypse,
                       [canvas_element, custom_styling, chart],
                       "Apocalypse", model_params)
