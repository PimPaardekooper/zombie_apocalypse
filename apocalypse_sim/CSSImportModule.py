from mesa.visualization.ModularVisualization import VisualizationElement

class CSSImportModule(VisualizationElement):
    local_includes = ["CSSImportModule.js"]

    def __init__(self):
        self.js_code = "elements.push(new CSSImportModule());"

    def render(self, model):
        return {}
