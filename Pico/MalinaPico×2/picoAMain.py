from machine import Pin, UART, PWM
from time import sleep_ms, ticks_ms, ticks_diff

uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
bzucak = PWM(Pin(16))
bzucak.freq(1000)
bzucak.duty_u16(0)

vzdalenost = -1
zvuk = False
posledni_zmena = ticks_ms()

def nastav_zvuk(zapnout):
    global zvuk
    zvuk = zapnout
    bzucak.duty_u16(32768 if zapnout else 0)

try:
    while True:
        # přečíst nejnovější hodnotu ze senzoru
        while uart.any():
            radek = uart.readline()
            try:
                vzdalenost = int(radek.decode().strip())
                print("Vzdalenost:", vzdalenost, "cm")
            except:
                pass

        if vzdalenost < 0 or vzdalenost > 50:
            nastav_zvuk(False)                 # daleko nebo mimo rozsah: ticho
        elif vzdalenost < 5:
            nastav_zvuk(True)                  # velmi blízko: souvislý tón
        else:
            interval = vzdalenost * 15         # 50 cm = 750 ms, 10 cm = 150 ms
            if ticks_diff(ticks_ms(), posledni_zmena) >= (80 if zvuk else interval):
                nastav_zvuk(not zvuk)          # pípnutí 80 ms, pak pauza
                posledni_zmena = ticks_ms()

        sleep_ms(10)
finally:
    bzucak.duty_u16(0)