from layer import Layer

class Sublayer(Layer):
    def __init__(self, parent):
        Layer.__init__(self, parent.context, parent.color)
        self.parent = parent
