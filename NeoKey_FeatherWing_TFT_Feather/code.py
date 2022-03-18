"""
CircuitPython Timestamper for NeoKey FeatherWing.

To use the timestamper:
- First, press the second key (lit up teal by default) to start the timer. While the timer is
running, the NeoPixel under the second key will pulse.
- Once the timer is running, press the first key (lit up purple by default) to type out the
timestamp.
"""
import time
import math
import board
import usb_hid
import keypad
import neopixel
import terminalio
from displayio import Group
from adafruit_display_text.bitmap_label import Label
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.helper import PixelMap
from adafruit_led_animation.color import PURPLE, TEAL

display = board.DISPLAY

# create label to show the time on the display
lbl = Label(terminalio.FONT, scale=4)
lbl.anchor_point = (0.5, 0.5)
lbl.anchored_position = (display.width // 2, display.height // 2)

# create a Group to show on the display
main_group = Group()
# add the label to it
main_group.append(lbl)
# show the group
display.show(main_group)

# initial text is 0 minutes 0 seconds
lbl.text = "00:00"

# NeoPixel set up.
pixels = neopixel.NeoPixel(board.D9, 2)
# Light up the first key purple, and the second key teal. Remember, Python begins
# counting at 0, so the first pixel is 0, and the second pixel is 1.
pixels[0] = PURPLE
pixels[1] = TEAL

# Set up to pulse timer start key when timer is running.
timer_pixel = PixelMap(pixels, (1,), individual_pixels=True)
timer_pulse = Pulse(timer_pixel, speed=0.01, color=TEAL, period=4)

# Create keys object.
keys = keypad.Keys((board.D5, board.D6), value_when_pressed=False, pull=True)

# Create keyboard object and keyboard.
keyboard_object = Keyboard(usb_hid.devices)
keyboard = KeyboardLayoutUS(keyboard_object)

# Start timestamp at 00:00
TIMESTAMP = "00:00"

# Initiate start and current time variables.
START_TIME = None
CURRENT_TIME = None

while True:
    CURRENT_TIME = time.monotonic()
    # Begin monitoring for key events, i.e. key presses.
    key_event = keys.events.get()
    if key_event:  # If there is an event...
        if key_event.pressed:  # Specifically a key pressed...
            print(key_event.key_number)  # Print the key number to the serial console.
            # If the second key is pressed and START_TIME is None...
            if key_event.key_number == 1 and START_TIME is None:
                START_TIME = time.monotonic()  # Set START_TIME to time.monotonic().
            # If the first key is pressed and START_TIME is anything other than None...
            elif key_event.key_number == 0 and START_TIME:
                # Write out the timestamp into the active document.
                keyboard.write(lbl.text)
    if START_TIME:  # If START_TIME is anything but None, meaning the timer is running...
        timer_pulse.animate()  # Animate a pulse on timer start key to indicate timer is active.

        # update the showing time
        elapsed = CURRENT_TIME - START_TIME
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
