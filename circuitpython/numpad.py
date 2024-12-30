import board
import displayio
import terminalio
from adafruit_display_text import bitmap_label as label
from layer import Layer

class Numpad(Layer):
    def __init__(self, context):
        Layer.__init__(self, context, (50, 30, 10))
        text_group = displayio.Group()
        font = terminalio.FONT
        for i in range(5):
            line = label.Label(
                font,
                text = " ",
                anchor_point = (0,0),
                anchored_position = (0, 12 * i)
            )
            text_group.append(line)
        self.text_group = text_group

    def keyEvent(self, key_event):
        macropad = self.context.macropad
        if key_event.pressed:
            if key_event.key_number == 0:
                self.context.bridge.write("7")
            if key_event.key_number == 1:
                self.context.bridge.write("8")
            if key_event.key_number == 2:
                self.context.bridge.write("9")
            if key_event.key_number == 3:
                self.context.bridge.write("4")
            if key_event.key_number == 4:
                self.context.bridge.write("5")
            if key_event.key_number == 5:
                self.context.bridge.write("6")
            if key_event.key_number == 6:
                self.context.bridge.write("1")
            if key_event.key_number == 7:
                self.context.bridge.write("2")
            if key_event.key_number == 8:
                self.context.bridge.write("3")
            if key_event.key_number == 9:
                self.context.bridge.write("0")
            if key_event.key_number == 10:
                self.context.bridge.write("E")
            if key_event.key_number == 11:
                self.context.bridge.write(",")
                # macropad.keyboard.send(macropad.Keycode.PERIOD)

    def name(self):
        return " NUMPAD"

    def shortName(self):
        return " NP"

    def rotated(self, delta):
        context = self.context
        brite = context.brite
        brite_index = context.brite_index
        brite_index += delta
        if brite_index < 0:
            brite_index = 0
        elif brite_index >= len(brite):
            brite_index = len(brite) - 1
        context.brite_index = brite_index
        context.pixels.brightness = brite[brite_index]

    def display(self):
        self.context.macropad.display_sleep = False
        text_lines = self.text_group
        text_lines[0].text = "       NUMPAD  brite"
        text_lines[1].text = "   7      8      9"
        text_lines[2].text = "   4      6      7"
        text_lines[3].text = "   1      2      3"
        text_lines[4].text = "   0    ENTER    ,"
        board.DISPLAY.root_group = text_lines
        self.context.pixels.fill(self.color)
