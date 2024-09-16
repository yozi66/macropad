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
            text = "-nn:nn",
            scale = 3,
            anchor_point = (0,0),
            anchored_position = (2,0)
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
        self.running = False
        self.remaining_millis = 25*60*1000
        self.last_remaining = self.remaining_millis
        self.last_tick = supervisor.ticks_ms()
        self.mute = False

    def activate(self):
        self.text_group[1].text = "  3:00  12:30  25:00"
        self.text_group[2].text = " MUSIC  TIMER   LOCK"
        board.DISPLAY.root_group = self.text_group

    def keyEvent(self, key_event):
        if key_event.pressed:
            macropad = self.context.macropad
            if not self.running:
                if key_event.key_number == 0:
                    self.remaining_millis = 5*60*1000
                if key_event.key_number == 1:
                    self.remaining_millis = 10*60*1000
                if key_event.key_number == 2:
                    self.remaining_millis = 50*60*1000
                if key_event.key_number == 3:
                    self.remaining_millis = 4*60*1000
                if key_event.key_number == 4:
                    self.remaining_millis = 15*60*1000
                if key_event.key_number == 5:
                    self.remaining_millis = 10*1000
                if key_event.key_number == 6:
                    self.remaining_millis = 3*60*1000
                if key_event.key_number == 7:
                    self.remaining_millis = (12*60+30)*1000
                if key_event.key_number == 8:
                    self.remaining_millis = 25*60*1000
            else:
                if key_event.key_number == 5:
                    self.mute = not self.mute
            if key_event.key_number == 9:
                macropad.consumer_control.send(
                    macropad.ConsumerControlCode.PLAY_PAUSE
                )
            if key_event.key_number == 10:
                self.running = not self.running
                if not self.running:
                    self.mute = False
            if key_event.key_number == 11:
                macropad.keyboard.press(macropad.Keycode.WINDOWS, macropad.Keycode.L)
                macropad.keyboard.release_all()

    def name(self):
        return " TIMER "

    def shortName(self):
        return " TM"

    def rotated(self, delta):
        macropad = self.context.macropad
        while(delta > 0):
            for i in range(3):
                macropad.consumer_control.send(
                    macropad.ConsumerControlCode.VOLUME_INCREMENT
                )
            delta -= 1

        while(delta < 0):
            for i in range(3):
                macropad.consumer_control.send(
                    macropad.ConsumerControlCode.VOLUME_DECREMENT
                )
            delta += 1

    def display(self):
        self.context.macropad.display_sleep = False
        text_group = self.text_group
        full_seconds = self.seconds()
        negative = full_seconds < 0
        minutes = 0
        minutes = full_seconds // 60
        seconds = full_seconds % 60
        prefix = " "
        if negative:
            prefix = "-"
            minutes = -1 - minutes
            seconds = 60 - seconds
            if (seconds == 60):
                seconds = 0
                minutes += 1
        text_group[0].text = "%s%2d:%02d" % (prefix, minutes, seconds)
        self.context.pixels.fill(self.color)
        if self.running:
            color = self.green
            if self.remaining_millis < 500:
                color = self.red
            for i in range(9):
                self.context.pixels[i] = color
            self.context.pixels[10] = color
            if self.mute:
                color2 = self.color
                if color == self.red:
                    color2 = self.green
                self.context.pixels[5] = color2

    def seconds(self):
        return (self.remaining_millis) // 1000

    def tick(self, ms):
        result = False
        tone = False
        if self.running:
            old_seconds = self.seconds()
            delta = ms - self.last_tick
            self.remaining_millis -= delta
            seconds = self.seconds()
            if seconds != old_seconds:
                result = True # ask for display refresh
            # beep at 0, -60, -120, etc seconds for 3 x 100 ms with 100 ms break
            if seconds <= 0:
                if (-seconds % 60 == 0):
                    slice = (-self.remaining_millis % 1000) // 100
                    tone = slice in (0, 2, 4)
            # beep every 15 minutes if muted
            if (self.mute and -seconds % 900 != 0):
                tone = False
        if tone:
            self.context.macropad.start_tone(2000)
        else:
            self.context.macropad.stop_tone()

        # pixel color change at 500 ms
        if self.last_remaining >= 500 and self.remaining_millis < 500:
            result = True
        self.last_remaining = self.remaining_millis

        self.last_tick = ms
        return result
