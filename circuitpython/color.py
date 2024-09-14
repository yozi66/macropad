from sublayer import Sublayer

class Color(Sublayer):
    def __init__(self, parent, index):
        Sublayer.__init__(self, parent)
        self.index = index

    def name(self):
        parentName = self.parent.shortName()
        index = self.index
        if (index == 0):
            return parentName + "red "
        if (index == 1):
            return parentName + "grn "
        if (index == 2):
            return parentName + "blu "

    def rotated(self, delta):
        color = self.parent.color
        value = color[self.index]
        value += delta
        if (value < 0):
            value = 0
        elif (value > 255):
            value = 255
        self.setValue(value)

    def setValue(self, value):
        color = self.parent.color
        colorList = [color[0], color[1], color[2]]
        colorList[self.index] = value
        color = (colorList[0], colorList[1], colorList[2])
        self.parent.color = color

    def display(self):
        context = self.context
        context.macropad.display_sleep = False
        text_lines = context.text_lines
        text_lines[0].text = self.name() + ": " + str(self.parent.color)
        text_lines[1].text = "   70     80     90"
        text_lines[2].text = "   40     50     60"
        text_lines[3].text = "   10     20     30"
        text_lines[4].text = "    0      2      5"
        self.context.pixels.fill(self.parent.color)

    def keyEvent(self, key_event):
        if key_event.pressed:
            values = [70, 80, 90, 40, 50, 60, 10, 20, 30, 0, 2, 5]
            self.setValue(values[key_event.key_number])

