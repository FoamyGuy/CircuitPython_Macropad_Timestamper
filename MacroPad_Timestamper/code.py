import time

import math
import board
import usb_hid
import terminalio
from displayio import Group
from adafruit_display_text.bitmap_label import Label
from adafruit_macropad import MacroPad
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

kbd = Keyboard(usb_hid.devices)
kbd_lyt = KeyboardLayoutUS(kbd)

macropad = MacroPad()

lbl = Label(terminalio.FONT, scale=2)
lbl.y = 20
display = board.DISPLAY

main_group = Group()
main_group.append(lbl)
display.show(main_group)

lbl.text = "00:00"

macropad.pixels[2] = 0x00FF00

macropad.pixels[11] = 0x0000FF

START_TIME = None
CUR_TIME = None
while True:
    CUR_TIME = time.monotonic()
    key_event = macropad.keys.events.get()
    if key_event:
        if key_event.pressed:
            print(key_event.key_number)
            if key_event.key_number == 2:
                if START_TIME is None:
                    START_TIME = time.monotonic()
            elif key_event.key_number == 11 and START_TIME:
                kbd_lyt.write(lbl.text)
    if START_TIME:
        elapsed = CUR_TIME - START_TIME
        elapsed_min = elapsed // 60
        elapsed_sec = elapsed % 60
        _time_str = f"{int(elapsed_min):02}:{math.floor(elapsed_sec):02} "
        if lbl.text != _time_str:
            lbl.text = _time_str
