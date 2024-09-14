from layer import Layer

class Off(Layer):
    def __init__(self, context):
        Layer.__init__(self, context, (0,0,0))

    def display(self):
        context = self.context
        context.macropad.display_sleep = True
        context.pixels.fill(self.color)

    def name(self):
        return "  OFF  "
