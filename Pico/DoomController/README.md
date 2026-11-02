# DoomController

Raspberry Pi Pico se po USB hlásí Raspberry Pi jako standardní HID klávesnice.
Analogový joystick ovládá pohyb a tlačítka posílají klávesy, které používá
klasické rozložení hry Doom. Na Raspberry Pi se proto nemusí instalovat žádný
speciální ovladač.

## Hardware

- Raspberry Pi 4 Model B
- Raspberry Pi Pico nebo Pico H s konektorem micro-USB
- analogový joystickový modul s výstupy `VRx`, `VRy` a `SW`
- šest samostatných tlačítek
- propojovací vodiče a nepájivé pole

## Zapojení

Všechny signály joysticku a tlačítek pracují s 3,3 V. Nepřipojuj analogové
výstupy joysticku k 5 V.

| Ovladač | Pico | Funkce ve hře |
| --- | --- | --- |
| Joystick `VRx` | GP26 / ADC0 | Doleva a doprava |
| Joystick `VRy` | GP27 / ADC1 | Dopředu a dozadu |
| Joystick `VCC` | 3V3(OUT) | Napájení joysticku |
| Joystick `GND` | GND | Zem |
| Tlačítko A | GP2 a GND | Střelba (Ctrl) |
| Tlačítko B | GP3 a GND | Použít / otevřít (Space) |
| Tlačítko X | GP4 a GND | Modifikátor úkroku (Alt) |
| Tlačítko Y | GP5 a GND | Běh (Shift) |
| Tlačítko START | GP6 a GND | Potvrdit (Enter) |
| Tlačítko BACK | GP7 a GND | Menu (Esc) |
| Kliknutí joysticku `SW` | GP8 a GND | Mapa (Tab) |

Tlačítka se připojují mezi uvedený GPIO a GND; firmware zapíná interní
pull-up rezistory. U joystickového modulu připoj také `SW` mezi GP8 a GND.
Všechny země musí být propojené. Pico se k Raspberry Pi připojí datovým USB
kabelem; kabel zároveň napájí Pico.

## Firmware Pico

Firmware používá CircuitPython a knihovnu `adafruit_hid`:

1. Nainstaluj na Pico aktuální CircuitPython UF2 pro Raspberry Pi Pico.
2. Z balíčku CircuitPython Library Bundle zkopíruj složku `adafruit_hid` do
   `CIRCUITPY/lib/`.
3. Zkopíruj soubor [code.py](code.py) do kořene jednotky `CIRCUITPY`.
4. Při připojení nebo restartu Pico nech joystick prvních přibližně 320 ms
   uprostřed, aby firmware změřil jeho střed.

Prahová hodnota osy je nastavena na 12000 z rozsahu ADC 0–65535. Pokud se
joystick po uvolnění samovolně pohybuje, zkontroluj jeho zapojení a případně
zvětši `AXIS_THRESHOLD` v `code.py`.

## Doom na Raspberry Pi

Nainstaluj Chocolate Doom a spusť ho s IWAD souborem, který smíš používat.
Původní herní data Doom nejsou součástí tohoto projektu; použij vlastní
legálně získaný soubor `DOOM.WAD`. Alternativně lze ověřit ovladač s
bezplatnými daty Freedoom.

```sh
sudo apt update
sudo apt install chocolate-doom freedoom
chocolate-doom -iwad /cesta/k/DOOM.WAD
```

Po připojení se Pico chová jako klávesnice. Výchozí klávesy klasického Doomu
odpovídají ovladači v tabulce. Pokud už jsou ve hře změněné, uprav je v
nastavení ovládání Doom nebo změň přiřazení v `BUTTON_KEYS` a směrové klávesy
v `code.py`.
