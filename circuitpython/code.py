# SPDX-FileCopyrightText: 2021 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
"""
MacroPad HID keyboard and mouse demo. The demo sends "a" when the first key is pressed, a "B" when
the second key is pressed, "Hello, World!" when the third key is pressed, and decreases the volume
when the fourth key is pressed. It sends a right mouse click when the rotary encoder switch is
pressed. Finally, it moves the mouse left and right when the rotary encoder is rotated
counterclockwise and clockwise respectively.
"""
from adafruit_macropad import MacroPad

macropad = MacroPad()

BRITE = "BRITE"
COLOR = "COLOR"
VOLUME = "VOLUME"
OFF = "OFF"
modes = [BRITE, VOLUME, COLOR, OFF]
blue = 128
colors = [(255,255,blue), (255,255,0), (255,255,blue), (0,0,0)]
mode_index = 0
mode = modes[mode_index]

last_position = 0


brite = [0.0, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0]
brite_index = 2;
pixels = macropad.pixels
pixels.brightness = brite[brite_index]

text_lines = macropad.display_text()

def display():
    if mode == OFF:
        macropad.display_sleep = True
    else:
        macropad.display_sleep = False
        space = "        "
        text_lines[1].text = space + mode
        text_lines[2].text = space + "pos: " + str(last_position)
        text_lines[3].text = space + "brt: " + str(brite_index)
        text_lines[4].text = space + "blu: " + str(blue)
        text_lines.show()
    pixels.fill(colors[mode_index])

display()

while True:
    key_event = macropad.keys.events.get()

    if key_event and mode != OFF:
        if key_event.pressed:
            if key_event.key_number == 0:
                macropad.keyboard.send(macropad.Keycode.SEVEN)
            if key_event.key_number == 1:
                macropad.keyboard.send(macropad.Keycode.EIGHT)
            if key_event.key_number == 2:
               macropad.keyboard.send(macropad.Keycode.NINE)
            if key_event.key_number == 3:
                macropad.keyboard.send(macropad.Keycode.FOUR)
            if key_event.key_number == 4:
                macropad.keyboard.send(macropad.Keycode.FIVE)
            if key_event.key_number == 5:
                macropad.keyboard.send(macropad.Keycode.SIX)
            if key_event.key_number == 6:
                macropad.keyboard.send(macropad.Keycode.ONE)
            if key_event.key_number == 7:
                macropad.keyboard.send(macropad.Keycode.TWO)
            if key_event.key_number == 8:
                macropad.keyboard.send(macropad.Keycode.THREE)
            if key_event.key_number == 9:
                if mode == VOLUME:
                    macropad.consumer_control.send(
                        macropad.ConsumerControlCode.PLAY_PAUSE
                    )
                else:
                    macropad.keyboard.send(macropad.Keycode.GRAVE_ACCENT) # ZERO in HU keyboard
            if key_event.key_number == 10:
                macropad.keyboard.send(macropad.Keycode.ENTER)
            if key_event.key_number == 11:
                macropad.keyboard.send(macropad.Keycode.COMMA)
                # macropad.keyboard.send(macropad.Keycode.PERIOD)
    macropad.encoder_switch_debounced.update()

    if macropad.encoder_switch_debounced.pressed:
        mode_index += 1
        if mode_index >= len(modes):
            mode_index = 0
        mode = modes[mode_index]
        display()

    current_position = macropad.encoder
    if current_position != last_position:
        delta = current_position - last_position
        last_position = current_position

        if mode == COLOR:
            blue += delta
            if (blue < 0):
                blue = 0
            elif (blue > 255):
                blue = 255
            color = (255,255, blue)
            colors[0] = color
            colors[mode_index] = color

        if mode == VOLUME:
            if delta > 0:
                macropad.consumer_control.send(
                    macropad.ConsumerControlCode.VOLUME_INCREMENT
                )
            else:
                macropad.consumer_control.send(
                    macropad.ConsumerControlCode.VOLUME_DECREMENT
                )

        if mode == BRITE:
            brite_index += delta
            if brite_index < 0:
                brite_index = 0
            elif brite_index >= len(brite):
                brite_index = len(brite) - 1
            pixels.brightness = brite[brite_index]

        display()

