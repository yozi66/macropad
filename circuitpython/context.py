from layer import Layer

class Context:
    def __init__(self, macropad):
        self.macropad = macropad
        self.text_lines = macropad.display_text()
        self.pixels = macropad.pixels
        self.brite = [0.0, 0.1, 0.2, 0.5, 1.0]
        self.brite_index = 2;
        self.layerIndex = 9
        self.switch = ContextSwitch(self)
        self.layers = []

    def display(self):
        self.pixels.brightness = self.brite[self.brite_index]
        layer = self.layers[self.layerIndex]
        layer.display()

    def buttonPress(self):
        self.switch.buttonPress()

    def keyEvent(self, key_event):
        layer = self.layers[self.layerIndex]
        layer.keyEvent(key_event)

    def rotated(self, delta):
        layer = self.layers[self.layerIndex]
        layer.rotated(delta)

    def layerName(self):
        return self.layers[self.layerIndex].name()

class ContextSwitch(Layer):
    def __init__(self, context):
        Layer.__init__(self, context, (60,0,0))

    def buttonPress(self):
        context = self.context
        if(self not in context.layers):
            context.layers.append(self)
        context.layerIndex = context.layers.index(self)

    def display(self):
        context = self.context
        context.macropad.display_sleep = False
        text_lines = context.text_lines
        text_lines[0].text = "   SELECT LAYER"
        text_lines[1].text = self.names(0)
        text_lines[2].text = self.names(3)
        text_lines[3].text = self.names(6)
        text_lines[4].text = self.names(9)
        context.pixels.fill(self.color)

    def names(self, index):
        result = ""
        for i in range(index, index + 3):
            result += self.context.layers[i].name()
        return result

    def name(self):
        return "SWITCH"

    def shortName(self):
        return " SW"

    def keyEvent(self, key_event):
        if key_event.pressed:
            self.context.layerIndex = key_event.key_number
            print("switched to ", self.context.layerName())
