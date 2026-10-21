import smbus
from time import sleep
from datetime import datetime
from gpiozero import CPUTemperature

class LCD:
    def __init__(self, sbernice=1, adresa=0x27):
        self.bus = smbus.SMBus(sbernice)
        self.adresa = adresa
        self.podsviceni = 0x08
        sleep(0.05)
        for nibble in (0x30, 0x30, 0x30, 0x20):   # inicializace do 4bit režimu
            self._posli_nibble(nibble, 0)
            sleep(0.005)
        self._prikaz(0x28)   # 4bit, 2 řádky
        self._prikaz(0x0C)   # displej zapnutý, bez kurzoru
        self._prikaz(0x06)   # posun kurzoru doprava
        self.smaz()

    def _zapis(self, data):
        self.bus.write_byte(self.adresa, data | self.podsviceni)

    def _posli_nibble(self, data, rs):
        self._zapis(data | rs | 0x04)   # E = 1
        sleep(0.0005)
        self._zapis(data | rs)          # E = 0
        sleep(0.0001)

    def _prikaz(self, hodnota):
        self._posli_nibble(hodnota & 0xF0, 0)
        self._posli_nibble((hodnota << 4) & 0xF0, 0)

    def _znak(self, hodnota):
        self._posli_nibble(hodnota & 0xF0, 1)
        self._posli_nibble((hodnota << 4) & 0xF0, 1)

    def smaz(self):
        self._prikaz(0x01)
        sleep(0.002)

    def text(self, retezec, radek):
        self._prikaz(0x80 if radek == 0 else 0xC0)
        for znak in retezec.ljust(16)[:16]:
            self._znak(ord(znak))

lcd = LCD()
cpu = CPUTemperature()

try:
    while True:
        lcd.text("Teplota CPU:", 0)
        lcd.text("{:.1f} C {}".format(cpu.temperature,
                 datetime.now().strftime("%H:%M:%S")), 1)
        sleep(1)
finally:
    lcd.smaz()