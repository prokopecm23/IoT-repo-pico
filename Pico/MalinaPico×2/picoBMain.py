from machine import Pin, UART, time_pulse_us
from time import sleep, sleep_us

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)

def zmer_vzdalenost():
    trig.value(0)
    sleep_us(2)
    trig.value(1)
    sleep_us(10)
    trig.value(0)
    doba = time_pulse_us(echo, 1, 30000)
    if doba < 0:
        return -1
    return int(doba * 0.0343 / 2)

while True:
    uart.write("{}\n".format(zmer_vzdalenost()))
    sleep(0.1)