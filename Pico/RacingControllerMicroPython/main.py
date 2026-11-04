import sys
import time

from machine import ADC, Pin, UART


with open("player.txt", "r") as config:
    player = config.read().strip()

if player not in ("1", "2"):
    raise ValueError("player.txt must contain 1 or 2")

x_axis = ADC(Pin(26))
y_axis = ADC(Pin(27))
buttons = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in range(2, 9)]
threshold = 12000

uart = None
if player == "1":
    uart = UART(0, baudrate=115200, tx=Pin(0), rx=Pin(1))


def read_center(axis):
    total = 0
    for _ in range(32):
        total += axis.read_u16()
        time.sleep_ms(5)
    return total // 32


def send_line(line):
    if uart is not None:
        uart.write(line)
    else:
        sys.stdout.write(line.decode())


print("Player", player, "- keep the joystick centered while it calibrates.")
x_center = read_center(x_axis)
y_center = read_center(y_axis)
print("Racing controller ready.")

while True:
    x_value = x_axis.read_u16()
    y_value = y_axis.read_u16()

    if x_value < x_center - threshold:
        steer = -1
    elif x_value > x_center + threshold:
        steer = 1
    else:
        steer = 0

    if y_value < y_center - threshold:
        throttle = 1
    elif y_value > y_center + threshold:
        throttle = -1
    else:
        throttle = 0

    button_mask = 0
    for index, button in enumerate(buttons):
        if button.value() == 0:
            button_mask |= 1 << index

    line = "{},{},{},{}\n".format(
        player, steer, throttle, button_mask
    ).encode()
    send_line(line)
    time.sleep_ms(20)
