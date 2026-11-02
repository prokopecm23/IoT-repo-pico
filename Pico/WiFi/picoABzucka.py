import network
import socket
from machine import Pin, PWM
from time import sleep, sleep_ms, ticks_ms, ticks_diff

bzucak = PWM(Pin(16))
bzucak.freq(1000)
bzucak.duty_u16(0)
led = Pin("LED", Pin.OUT)

ap = network.WLAN(network.AP_IF)
try:
    ap.config(ssid="Pico-Hotspot", key="Pico1234")
except:
    ap.config(essid="Pico-Hotspot", password="Pico1234")
ap.active(True)
while not ap.active():
    sleep(0.2)
led.on()   # svítí = WiFi síť běží
print("Hotspot bezi, IP:", ap.ifconfig()[0])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("0.0.0.0", 5000))
s.settimeout(0)   # neblokovat, aby bzučák mohl pípat

vzdalenost = -1
posledni_data = ticks_ms()
zvuk = False
posledni_zmena = ticks_ms()

def nastav_zvuk(zapnout):
    global zvuk
    zvuk = zapnout
    bzucak.duty_u16(32768 if zapnout else 0)

try:
    while True:
        # přečíst všechny čekající zprávy, nechat si tu nejnovější
        while True:
            try:
                data, adresa = s.recvfrom(64)
                vzdalenost = int(data.decode())
                posledni_data = ticks_ms()
                print("Vzdalenost:", vzdalenost, "cm")
            except OSError:
                break
            except ValueError:
                pass

        # když 1 s nepřišla žádná data, ztišit
        if ticks_diff(ticks_ms(), posledni_data) > 1000:
            vzdalenost = -1

        if vzdalenost < 0 or vzdalenost > 50:
            nastav_zvuk(False)
        elif vzdalenost < 5:
            nastav_zvuk(True)
        else:
            interval = vzdalenost * 15
            if ticks_diff(ticks_ms(), posledni_zmena) >= (80 if zvuk else interval):
                nastav_zvuk(not zvuk)
                posledni_zmena = ticks_ms()

        sleep_ms(10)
finally:
    bzucak.duty_u16(0)