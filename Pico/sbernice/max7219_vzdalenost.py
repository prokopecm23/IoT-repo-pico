from machine import Pin, SPI, time_pulse_us
import utime

# HC-SR04
TRIG_PIN = 14
ECHO_PIN = 15

# MAX7219 matice 8x8, SPI0
SPI_SCK_PIN = 18
SPI_MOSI_PIN = 19
MAX7219_CS_PIN = 17

MIN_DISTANCE_CM = 2
MAX_DISTANCE_CM = 40

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
spi = SPI(
    0,
    baudrate=1000000,
    polarity=0,
    phase=0,
    sck=Pin(SPI_SCK_PIN),
    mosi=Pin(SPI_MOSI_PIN),
)
cs = Pin(MAX7219_CS_PIN, Pin.OUT, value=1)


def max7219_write(register, value):
    cs.value(0)
    spi.write(bytes((register, value)))
    cs.value(1)


def max7219_init():
    max7219_write(0x0F, 0)  # display test off
    max7219_write(0x09, 0)  # no BCD decode
    max7219_write(0x0B, 7)  # use all 8 rows
    max7219_write(0x0A, 5)  # brightness: 0..15
    max7219_write(0x0C, 1)  # normal operation
    for row in range(1, 9):
        max7219_write(row, 0)


def read_distance_cm():
    trig.low()
    utime.sleep_us(2)
    trig.high()
    utime.sleep_us(10)
    trig.low()

    pulse_us = time_pulse_us(echo, 1, 30000)
    if pulse_us <= 0:
        return None

    distance_cm = pulse_us / 58.0
    if MIN_DISTANCE_CM <= distance_cm <= MAX_DISTANCE_CM:
        return distance_cm
    return None


def distance_to_led_count(distance_cm):
    distance_cm = min(MAX_DISTANCE_CM, max(MIN_DISTANCE_CM, distance_cm))
    lit = int(
        (MAX_DISTANCE_CM - distance_cm)
        * 64
        / (MAX_DISTANCE_CM - MIN_DISTANCE_CM)
        + 0.5
    )
    return min(64, max(0, lit))


def show_bar(led_count):
    for row_from_bottom in range(8):
        row_leds = min(8, max(0, led_count - row_from_bottom * 8))
        row_bits = (1 << row_leds) - 1 if row_leds else 0
        max7219_write(8 - row_from_bottom, row_bits)


max7219_init()

while True:
    distance = read_distance_cm()
    if distance is None:
        show_bar(0)
        print("No echo / out of range")
    else:
        led_count = distance_to_led_count(distance)
        show_bar(led_count)
        print("Distance: {:.1f} cm, LEDs: {}".format(distance, led_count))

    utime.sleep_ms(100)