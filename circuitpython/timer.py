import board
import displayio
import supervisor
import terminalio
from adafruit_display_text import bitmap_label as label
from layer import Layer

class Timer(Layer):
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    def __init__(self, context):
        Layer.__init__(self, context, (40, 20, 0))
        self.red = (60, 0, 0)
        self.green = (0, 40, 0)
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
        self.running = True
        self.expired = False
        self.remaining_millis = 10*1000
        self.last_tick = supervisor.ticks_ms()

    def keyEvent(self, key_event):
        macropad = self.context.macropad
        if key_event.pressed and key_event.key_number == 9:
            macropad.consumer_control.send(
                macropad.ConsumerControlCode.PLAY_PAUSE
            )
        if key_event.pressed and key_event.key_number == 11:
            macropad.keyboard.press(macropad.Keycode.WINDOWS, macropad.Keycode.L)
            macropad.keyboard.release_all()
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

    def activate(self):
        self.text_group[1].text = "  4:00  12:30 [25:00]"
        self.text_group[2].text = " MUSIC  START   LOCK"
        board.DISPLAY.root_group = self.text_group

    def display(self):
        self.context.macropad.display_sleep = False
        text_group = self.text_group
        full_seconds = self.seconds()
        negative = full_seconds < 0
        minutes = 0
        minutes = full_seconds // 60
        seconds = full_seconds % 60
        if negative:
            minutes = -1 - minutes
            seconds = 60 - seconds
            if (seconds == 60):
                seconds = 0
                minutes += 1
        text_group[0].text = "%02d:%02d" % (minutes, seconds)
        self.context.pixels.fill(self.color)
        if self.running:
            color = self.red
            if self.remaining_millis > 0:
                color = self.green
            # self.context.pixels[8] = color
            for i in range(9):
                self.context.pixels[i] = color

    def seconds(self):
        return (self.remaining_millis + 999) // 1000 # round up

    def tick(self, ms):
        result = False
        if self.running:
            old_seconds = self.seconds()
            delta = ms - self.last_tick
            self.remaining_millis -= delta
            if self.seconds() != old_seconds:
                result = True
        self.last_tick = ms
        return result
