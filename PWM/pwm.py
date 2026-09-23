from machine import Pin, PWM, ADC
import utime

# Potenciometr na ADC0 (GP26)
POT_PIN = 26
BUZZER_PIN = 16

pot = ADC(Pin(POT_PIN))
buzzer = PWM(Pin(BUZZER_PIN))
buzzer.duty_u16(30000)

last_freq = 500

while True:
    raw = pot.read_u16()
    target_freq = 200 + int((raw / 65535) * 1800)

    if last_freq < target_freq:
        last_freq = min(target_freq, last_freq + 25)
    elif last_freq > target_freq:
        last_freq = max(target_freq, last_freq - 25)

    buzzer.freq(last_freq)
    utime.sleep_ms(20)
