try:
    from machine import Pin  # type: ignore[import-not-found]
    import utime  # type: ignore[import-not-found]
except ImportError:
    class Pin:
        OUT = "OUT"
        IN = "IN"
        PULL_UP = "PULL_UP"

        def __init__(self, pin_id, mode=None, pull=None):
            self.pin_id = pin_id
            self.mode = mode
            self.pull = pull

        def value(self, val=None):
            return 1

        def off(self):
            pass

        def on(self):
            pass

    class _Utime:
        @staticmethod
        def sleep_ms(ms):
            pass

    utime = _Utime()


# Raspberry Pi Pico
# External LED on GP16
# External button on GP15, connected to GND
LED_PIN = 16
BUTTON_PIN = 15

led = Pin(LED_PIN, Pin.OUT)
button = Pin(BUTTON_PIN, Pin.IN, Pin.PULL_UP)

print("Pico ready. Hold the button to blink the LED.")

while True:
    if button.value() == 0:
        led.on()
        utime.sleep_ms(150)
        led.off()
        utime.sleep_ms(150)
    else:
        led.off()
        utime.sleep_ms(20)
