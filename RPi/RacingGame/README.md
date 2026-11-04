# Pico Kart

Závod pro dva hráče na jednom Raspberry Pi 4 se split-screen pohledem. Oba
ovladače používají MicroPython: hráč 1 komunikuje přes UART GPIO a hráč 2 přes
USB sériový port.

## Zapojení ovladačů

Stejné zapojení joysticku a tlačítek použij na obou Pico. Analogové vstupy
pracují s 3,3 V; nepřipojuj je na 5 V.

| Součást | Pin Pico |
| --- | --- |
| Joystick `VRx` | GP26 / ADC0 |
| Joystick `VRy` | GP27 / ADC1 |
| Joystick `VCC` | 3V3(OUT) |
| Joystick `GND` | GND |
| Tlačítko A – zrychlení | GP2 a GND |
| Tlačítko B – drift | GP3 a GND |
| Tlačítko X – použít bonus | GP4 a GND |
| Tlačítko Y – klakson | GP5 a GND |
| Tlačítko START – pauza | GP6 a GND |
| Tlačítko BACK – restart závodu | GP7 a GND |
| Kliknutí joysticku – pauza | GP8 a GND |

Tlačítka se zapojují mezi GPIO a GND; firmware používá interní pull-up
rezistory.

### Pico hráče 1 – UART

Zapoj UART křížem mezi Pico a Raspberry Pi:

| Raspberry Pi 4 | Fyzický pin Pi | Pico hráče 1 |
| --- | --- | --- |
| GPIO14 / TXD | 8 | GP1 / UART0 RX |
| GPIO15 / RXD | 10 | GP0 / UART0 TX |
| GND | 6 | GND |

Signály UART jsou 3,3 V. Nepropojuj 5V pin Pi s GPIO Pico. UART používá
výchozí `/dev/serial0` na Raspberry Pi.

### Pico hráče 2 – USB sériový port

Připoj Pico hráče 2 datovým USB kabelem přímo k Raspberry Pi. MicroPython
vysílá ovládání přes USB sériovou konzoli; nejde o USB HID klávesnici.
Výchozí zařízení je `/dev/ttyACM0`.

## Nahrání MicroPython programu

Nainstaluj MicroPython pro Raspberry Pi Pico na obě desky. Program lze nahrát
přes Thonny nebo `mpremote`.

1. Zkopíruj [main.py](../../Pico/RacingControllerMicroPython/main.py) do
   kořene Pico.
2. Na Pico hráče 1 ulož do kořene soubor `player.txt` s jediným znakem `1`.
3. Na Pico hráče 2 ulož do kořene soubor `player.txt` s jediným znakem `2`.
4. Restartuj obě desky a nech joysticky při startu uprostřed přibližně
   320 ms.

Příklady nahrání pomocí `mpremote` (nahraď `COM5`/`COM6` skutečnými porty
Pico ve Windows; na Raspberry Pi můžeš použít například `/dev/ttyACM0`):

```sh
mpremote connect COM5 fs cp Pico/RacingControllerMicroPython/main.py :main.py
mpremote connect COM5 fs cp Pico/RacingControllerMicroPython/player1.txt :player.txt
mpremote connect COM6 fs cp Pico/RacingControllerMicroPython/main.py :main.py
mpremote connect COM6 fs cp Pico/RacingControllerMicroPython/player2.txt :player.txt
```

Porty `COM5` a `COM6` jsou pouze příklady. Při nahrávání měj připojené jen
jedno Pico, nebo ověř v systému, který COM port patří které desce.

## Nastavení Raspberry Pi a spuštění

1. V `sudo raspi-config` otevři **Interface Options → Serial Port**.
2. Povol hardware serial port a zakaž login shell přes sériový port.
3. Restartuj Raspberry Pi.
4. Nainstaluj závislosti a spusť hru:

```sh
sudo apt update
sudo apt install python3-pygame python3-serial
cd RPi/RacingGame
python3 main.py
```

Pokud uživatel nemá oprávnění k sériovým portům, přidej ho do skupiny
`dialout` a potom se odhlaš a znovu přihlas:

```sh
sudo usermod -aG dialout "$USER"
```

Pokud USB Pico není `/dev/ttyACM0`, zjisti jeho zařízení pomocí `ls /dev/ttyACM*`
a předej správný port:

```sh
python3 main.py --uart-port /dev/serial0 --usb-port /dev/ttyACM1
```

Hra se otevře přes celou obrazovku. `Esc` pozastaví hru; START na kterémkoli
ovladači ji také pozastaví. BACK na ovladači restartuje závod. Vyhrává první
hráč, který dokončí tři kola.
