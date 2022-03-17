"""
CircuitPython Timestamper for Macropad.

To use the timestamper:
- First, press the top right key (lit up green by default) to start the timer. While the timer is
running, the current elapsed time will show on the macropad display.
- Once the timer is running, press the bottom right key (lit up blue by default) to type out the
timestamp.
"""
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

# Create keyboard object and keyboard.
kbd = Keyboard(usb_hid.devices)
kbd_lyt = KeyboardLayoutUS(kbd)

# initialize macropad helper library
macropad = MacroPad()

# create label to show the time on the display
lbl = Label(terminalio.FONT, scale=2)
lbl.y = 20

# we're using the build-in display
display = board.DISPLAY

# create a Group to show on the display
main_group = Group()
# add the label to it
main_group.append(lbl)
# show the group
display.show(main_group)

# initial text is 0 minutes 0 seconds
lbl.text = "00:00"

# set the color of the two buttons used
macropad.pixels[2] = 0x00FF00
macropad.pixels[11] = 0x0000FF

# Initiate start and current time variables.
START_TIME = None
CUR_TIME = None

while True:
    CUR_TIME = time.monotonic()
    # check for key press events
    key_event = macropad.keys.events.get()
    if key_event:  # If there is an event
        if key_event.pressed:  # Specifically a key pressed...
            print(key_event.key_number)  # print the number of the key

            # if it's the start key
            if key_event.key_number == 2:
                # if it wasn't already counting
                if START_TIME is None:
                    # Set START_TIME to now
                    START_TIME = time.monotonic()

            # If the timestamp key is pressed and START_TIME is anything other than None...
            elif key_event.key_number == 11 and START_TIME:
                # Write out the timestamp into the active document.
                kbd_lyt.write(lbl.text)

    # If START_TIME is anything but None, meaning the timer is running...
    if START_TIME:
        # update the
        elapsed = CUR_TIME - START_TIME
        # breakout hours, minutes, and seconds
        elapsed_hour = elapsed // 3600
        elapsed_min = (elapsed - (elapsed_hour * 3600)) // 60
        elapsed_sec = elapsed % 60
        if elapsed_hour == 0:  # no full hours yet
            # Generate a string of the human-readable elapsed time in minutes and seconds.
            time_string = f"{int(elapsed_min):02}:{math.floor(elapsed_sec):02} "
        else:  # at least 1 full hour
            # Generate a string of the human-readable elapsed time in hours minutes and seconds.
            time_string = f"{int(elapsed_hour):02}:{int(elapsed_min):02}:{math.floor(elapsed_sec):02} "

        # if the currently showing time is different than the real time
        if lbl.text != time_string:
            # update the showing time to current timestamp
            lbl.text = time_string
