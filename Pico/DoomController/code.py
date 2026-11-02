import time

import analogio
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


X_AXIS = analogio.AnalogIn(board.GP26)
Y_AXIS = analogio.AnalogIn(board.GP27)
AXIS_THRESHOLD = 12000
SCAN_INTERVAL = 0.01

BUTTON_KEYS = (
    (board.GP2, Keycode.CONTROL),  # Fire
    (board.GP3, Keycode.SPACE),  # Use/open
    (board.GP4, Keycode.ALT),  # Strafe modifier
    (board.GP5, Keycode.SHIFT),  # Run
    (board.GP6, Keycode.ENTER),  # Confirm
    (board.GP7, Keycode.ESCAPE),  # Menu
    (board.GP8, Keycode.TAB),  # Automap
)

buttons = []
for pin, key in BUTTON_KEYS:
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    buttons.append((button, key))

keyboard = Keyboard(usb_hid.devices)


def read_center(axis):
    total = 0
    for _ in range(32):
        total += axis.value
        time.sleep(0.005)
    return total // 32


print("Keep the joystick centered while it calibrates.")
x_center = read_center(X_AXIS)
y_center = read_center(Y_AXIS)
print("Doom controller ready.")

pressed_keys = set()

while True:
    x_value = X_AXIS.value
    y_value = Y_AXIS.value
    desired_keys = set()

    if x_value < x_center - AXIS_THRESHOLD:
        desired_keys.add(Keycode.LEFT_ARROW)
    elif x_value > x_center + AXIS_THRESHOLD:
        desired_keys.add(Keycode.RIGHT_ARROW)

    if y_value < y_center - AXIS_THRESHOLD:
        desired_keys.add(Keycode.UP_ARROW)
    elif y_value > y_center + AXIS_THRESHOLD:
        desired_keys.add(Keycode.DOWN_ARROW)

    for button, key in buttons:
        if not button.value:
            desired_keys.add(key)

    for key in pressed_keys - desired_keys:
        keyboard.release(key)
    for key in desired_keys - pressed_keys:
        keyboard.press(key)

    pressed_keys = desired_keys
    time.sleep(SCAN_INTERVAL)
