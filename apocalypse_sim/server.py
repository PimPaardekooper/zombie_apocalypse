"""server.py.

Visualizes the state of the model at a certain timestep,
defines what each object looks like given it's attributes and
adds user interaction to the model to change certain parameters
like initial population density. All code here is only written
to make the visual components of the used framework work properly,
but doesn't contribute to the actual project.
"""
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule, TextElement
from mesa.visualization.UserParam import UserSettableParameter
from gui_styling.CSSImportModule import CSSImportModule
from model_representation.portrayals import model_draw
from model_representation.mode import get_mode

import os
import webbrowser
import tornado.ioloop
import numpy as np

import random
import sys

from model import Apocalypse


class ModularServerExtd(ModularServer):
    """Used instead of ModularServer.

    This class overrides certain methods of the ModularServer
    from the mesa framework, since the ModularServer did not
    meet certain needs of ours. This was not important to the
    actual project, it was just to make our lives easier while
    working on it. We will therefore not document everything.

    """

    def __init__(self, model_cls, visualization_elements, name="Mesa Model",
                 model_params={}):
        """Initialize the server."""
        model_params['server'] = self
        self.verbose = False

        super().__init__(model_cls, visualization_elements, name, model_params)

    def launch(self, port=None):
        """Run the app."""
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


model_params, canvas_height, canvas_width, grid_height, grid_width = get_mode()
canvas_element = CanvasGrid(model_draw, grid_width,
                            grid_height, canvas_width, canvas_height)

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
