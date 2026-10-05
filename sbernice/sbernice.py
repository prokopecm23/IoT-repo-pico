from machine import I2C, Pin
import utime

# --- Konfigurace ---
TRIG_PIN = 14
ECHO_PIN = 15
I2C_SDA = 0
I2C_SCL = 1
LCD_ADDR = 0x27

# --- Inicializace I2C ---
i2c = I2C(0, sda=Pin(I2C_SDA), scl=Pin(I2C_SCL), freq=100000)

# --- LCD nastavení ---
LCD_BACKLIGHT = 0x08
LCD_ENABLE = 0x04
LCD_RS = 0x01

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)


def lcd_write_byte(data, mode=0):
    upper = (data & 0xF0) | mode | LCD_BACKLIGHT
    lower = ((data << 4) & 0xF0) | mode | LCD_BACKLIGHT

    i2c.writeto(LCD_ADDR, bytes([upper, upper | LCD_ENABLE, upper & ~LCD_ENABLE]))
    i2c.writeto(LCD_ADDR, bytes([lower, lower | LCD_ENABLE, lower & ~LCD_ENABLE]))
    utime.sleep_us(50)


def lcd_cmd(cmd):
    lcd_write_byte(cmd, 0)


def lcd_data(data):
    lcd_write_byte(data, LCD_RS)


def lcd_init():
    utime.sleep_ms(50)
    lcd_cmd(0x33)
    lcd_cmd(0x32)
    lcd_cmd(0x28)
    lcd_cmd(0x0C)
    lcd_cmd(0x06)
    lcd_cmd(0x01)
    utime.sleep_ms(2)


def lcd_gotoxy(x, y):
    if y == 0:
        lcd_cmd(0x80 + x)
    else:
        lcd_cmd(0xC0 + x)


def lcd_print(text):
    for ch in text:
        lcd_data(ord(ch))


def get_i2c_text():
    devices = i2c.scan()
    if not devices:
        return "I2C: none"

    text = "I2C:"
    for addr in devices:
        text += " " + hex(addr)
    return text[:16]


def read_distance_cm():
    trig.low()
    utime.sleep_us(2)
    trig.high()
    utime.sleep_us(10)
    trig.low()

    timeout_us = 25000
    start = utime.ticks_us()
    while echo.value() == 0:
        if utime.ticks_diff(utime.ticks_us(), start) > timeout_us:
            return None

    pulse_start = utime.ticks_us()
    start = utime.ticks_us()
    while echo.value() == 1:
        if utime.ticks_diff(utime.ticks_us(), start) > timeout_us:
            return None

    pulse_end = utime.ticks_us()
    pulse_us = utime.ticks_diff(pulse_end, pulse_start)
    if pulse_us <= 0:
        return None

    distance_cm = pulse_us / 58.0
    if 2 <= distance_cm <= 400:
        return distance_cm
    return None


print("I2C zařízení:", i2c.scan())

lcd_init()

while True:
    distance = read_distance_cm()
    bus_text = get_i2c_text()

    lcd_gotoxy(0, 0)
    lcd_print("                ")
    lcd_gotoxy(0, 0)
    lcd_print(bus_text)

    lcd_gotoxy(0, 1)
    lcd_print("                ")
    lcd_gotoxy(0, 1)
    if distance is None:
        lcd_print("Vzd: ERR")
    else:
        lcd_print(f"Vzd: {distance:5.1f} cm")

    utime.sleep_ms(200)
