from machine import UART, Pin
from time import sleep
 
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))
 
while True:
    if uart.any():
        zprava = uart.readline()
        if zprava:
            print("Prijato:", zprava.decode().strip())
    sleep(0.1)