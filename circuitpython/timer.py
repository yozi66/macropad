import board
import displayio
import terminalio
from adafruit_display_text import bitmap_label as label
from layer import Layer

class Timer(Layer):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    def __init__(self, context):
        Layer.__init__(self, context, (40, 20, 0))
        text_group = displayio.Group()
        font = terminalio.FONT
        big_label = label.Label(
            font,
            text = "25:00",
            scale = 3,
            anchor_point = (0,0),
            anchored_position = (20,0)
        )
        text_group.append(big_label)
        for i in range(2):
            line = label.Label(
                font,
                text = " ",
                anchor_point = (0,0),
                anchored_position = (0, 36 + 12 * i)
            )
            text_group.append(line)
        self.text_group = text_group

    def keyEvent(self, key_event):
        macropad = self.context.macropad
        if key_event.pressed and key_event.key_number == 9:
            macropad.consumer_control.send(
                macropad.ConsumerControlCode.PLAY_PAUSE
            )

    def name(self):
        return " TIMER "

    def shortName(self):
        return " TM"

    def rotated(self, delta):
        macropad = self.context.macropad
        while(delta > 0):
            macropad.consumer_control.send(
                macropad.ConsumerControlCode.VOLUME_INCREMENT
            )
            macropad.consumer_control.send(
                macropad.ConsumerControlCode.VOLUME_INCREMENT
            )
            delta -= 1

        while(delta < 0):
            macropad.consumer_control.send(
                macropad.ConsumerControlCode.VOLUME_DECREMENT
            )
            macropad.consumer_control.send(
                macropad.ConsumerControlCode.VOLUME_DECREMENT
            )
            delta += 1

    def display(self):
        self.context.macropad.display_sleep = False
        text_group = self.text_group
        text_group[1].text = " 60:00  30:00   3:00"
        text_group[2].text = " MUSIC  RESET   MUTE"
        board.DISPLAY.root_group = text_group
        self.context.pixels.fill(self.color)

