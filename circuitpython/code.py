from adafruit_macropad import MacroPad
from layer   import Layer
from context import Context, ContextSwitch
from timer   import Timer
from numpad  import Numpad
from off     import Off
from color   import Color

macropad = MacroPad()
context = Context(macropad)
switch = context.switch
timer = Timer(context)
numpad = Numpad(context)
context.layers = [
    Color(switch, 0), Color(switch, 1), Color(switch, 2),
    Color(numpad, 0), Color(numpad, 1), Color(numpad, 2),
    Color(timer, 0),  Color(timer, 1),  Color(timer, 2),
    timer, numpad, Off(context)
]

context.display()

# prepare for rotary encoder delta
last_position = 0

while True:
    key_event = macropad.keys.events.get()
    if (key_event):
        context.keyEvent(key_event)
        context.display()

    macropad.encoder_switch_debounced.update()
    if macropad.encoder_switch_debounced.pressed:
        context.buttonPress()
        context.display()

    current_position = macropad.encoder
    if current_position != last_position:
        delta = current_position - last_position
        last_position = current_position
        context.rotated(delta)
        context.display()
