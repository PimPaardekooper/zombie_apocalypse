"""Beautify framework visualization.

The framework provided a flawed GUI, such as
HTML elements with wrong widths. This code
attempts to fix these issues.
"""
from mesa.visualization.ModularVisualization import VisualizationElement

class CSSImportModule(VisualizationElement):
    local_includes = ["gui_styling/CSSImportModule.js"]

    def __init__(self):
        self.js_code = "elements.push(new CSSImportModule());"

    def render(self, model):
        return {}
