import time

import analogio
import board
import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode


with open("player.txt", "r") as config:
    player = config.read().strip()

if player not in ("1", "2"):
    raise ValueError("player.txt must contain 1 or 2")

X_AXIS = analogio.AnalogIn(board.GP26)
Y_AXIS = analogio.AnalogIn(board.GP27)
AXIS_THRESHOLD = 12000

if player == "1":
    LEFT = Keycode.A
    RIGHT = Keycode.D
    ACCELERATE = Keycode.W
    BRAKE = Keycode.S
    BUTTON_KEYS = (
        (board.GP2, Keycode.LEFT_SHIFT),
        (board.GP3, Keycode.SPACE),
        (board.GP4, Keycode.E),
        (board.GP5, Keycode.Q),
        (board.GP6, Keycode.ENTER),
        (board.GP7, Keycode.R),
        (board.GP8, Keycode.ENTER),
    )
else:
    LEFT = Keycode.LEFT_ARROW
    RIGHT = Keycode.RIGHT_ARROW
    ACCELERATE = Keycode.UP_ARROW
    BRAKE = Keycode.DOWN_ARROW
    BUTTON_KEYS = (
        (board.GP2, Keycode.RIGHT_SHIFT),
        (board.GP3, Keycode.RIGHT_ALT),
        (board.GP4, Keycode.RIGHT_CONTROL),
        (board.GP5, Keycode.RIGHT_BRACKET),
        (board.GP6, Keycode.ENTER),
        (board.GP7, Keycode.BACKSPACE),
        (board.GP8, Keycode.ENTER),
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


print("Player", player, "- keep the joystick centered while it calibrates.")
x_center = read_center(X_AXIS)
y_center = read_center(Y_AXIS)
print("Racing controller ready.")

pressed_keys = set()

while True:
    x_value = X_AXIS.value
    y_value = Y_AXIS.value
    desired_keys = set()

    if x_value < x_center - AXIS_THRESHOLD:
        desired_keys.add(LEFT)
    elif x_value > x_center + AXIS_THRESHOLD:
        desired_keys.add(RIGHT)

    if y_value < y_center - AXIS_THRESHOLD:
        desired_keys.add(ACCELERATE)
    elif y_value > y_center + AXIS_THRESHOLD:
        desired_keys.add(BRAKE)

    for button, key in buttons:
        if not button.value:
            desired_keys.add(key)

    for key in pressed_keys - desired_keys:
        keyboard.release(key)
    for key in desired_keys - pressed_keys:
        keyboard.press(key)

    pressed_keys = desired_keys
    time.sleep(0.01)
