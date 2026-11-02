import network
import socket
from machine import Pin, time_pulse_us
from time import sleep, sleep_us, time

trig = Pin(14, Pin.OUT)
echo = Pin(15, Pin.IN)
led = Pin("LED", Pin.OUT)

wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect("Pico-Hotspot", "Pico1234")

start = time()
while not wifi.isconnected():      # rychlé blikání = hledá síť
    led.toggle()
    if time() - start > 10:
        wifi.connect("Pico-Hotspot", "Pico1234")
        start = time()
    sleep(0.2)
led.on()                           # svítí = připojeno
print("Pripojeno:", wifi.ifconfig()[0])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server = ("192.168.4.1", 5000)

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
    s.sendto(str(zmer_vzdalenost()).encode(), server)
    sleep(0.1)