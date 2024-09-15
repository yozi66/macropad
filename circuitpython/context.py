from layer import Layer

class Context:
    def __init__(self, macropad):
        self.macropad = macropad
        self.text_lines = macropad.display_text()
        self.pixels = macropad.pixels
        self.brite = [0.0, 0.1, 0.2, 0.5, 1.0]
        self.brite_index = 2;
        self.layerIndex = 0
        self.layers = []

    def display(self):
        self.pixels.brightness = self.brite[self.brite_index]
        layer = self.layers[self.layerIndex]
        layer.display()

    def buttonPress(self):
        layerIndex = self.layerIndex
        layerIndex += 1
        if (layerIndex >= len(self.layers)):
            layerIndex = 0
        self.layerIndex = layerIndex
        print("switched to ", self.layerName())

    def keyEvent(self, key_event):
        layer = self.layers[self.layerIndex]
        layer.keyEvent(key_event)

    def rotated(self, delta):
        layer = self.layers[self.layerIndex]
        layer.rotated(delta)

    def layerName(self):
        return self.layers[self.layerIndex].name()
