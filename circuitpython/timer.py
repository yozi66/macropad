from layer import Layer

class Timer(Layer):
    def __init__(self, context):
        Layer.__init__(self, context, (40, 20, 0))

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
        text_lines = self.context.text_lines
        text_lines[0].text = "       TIMERS  volume"
        text_lines[1].text = " 15:00  20:00  25:00"
        text_lines[2].text = "  4:00   5:00  10:00"
        text_lines[3].text = " 60:00  30:00   3:00"
        text_lines[4].text = " MUSIC  RESET   MUTE"
        text_lines.show()
        self.context.pixels.fill(self.color)

