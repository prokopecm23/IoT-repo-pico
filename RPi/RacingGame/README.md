# Pico Kart

Jednoduchá lokální závodní hra pro dva hráče na jednom Raspberry Pi 4.
Každý hráč má vlastní polovinu obrazovky a vlastní Raspberry Pi Pico ovladač.
Hra používá vlastní kreslenou grafiku a zvuky nejsou potřeba.

## Potřebuješ

- Raspberry Pi 4 s Raspberry Pi OS a připojenou obrazovkou
- dva Raspberry Pi Pico (nebo Pico H) s analogovým joystickem a tlačítky
- dva datové USB kabely

Každé Pico se připojí vlastním USB kabelem k Raspberry Pi. Oba se hlásí jako
USB klávesnice, ale každý posílá jiné klávesy, takže hra rozpozná hráče 1 a 2.

## Zapojení ovladače

Zapoj oba ovladače stejně. Signály joysticku jsou 3,3V; nikdy na ně nepřiváděj
5 V.

| Ovladač | Pico | Funkce |
| --- | --- | --- |
| Joystick `VRx` | GP26 / ADC0 | Zatáčení doleva/doprava |
| Joystick `VRy` | GP27 / ADC1 | Plyn/brzda |
| Joystick `VCC` | 3V3(OUT) | Napájení |
| Joystick `GND` | GND | Zem |
| Tlačítko A | GP2 a GND | Krátké zrychlení |
| Tlačítko B | GP3 a GND | Drift |
| Tlačítko X | GP4 a GND | Použít sebrané zrychlení |
| Tlačítko Y | GP5 a GND | Klakson |
| Tlačítko START | GP6 a GND | Pauza / pokračování |
| Tlačítko BACK | GP7 a GND | Nový závod |
| Kliknutí joysticku `SW` | GP8 a GND | Pauza / pokračování |

Tlačítka se zapojují mezi GPIO a GND; firmware zapne interní pull-up. Země
joysticku a tlačítek musí být propojená s GND Pico.

## Nastavení Pico

Na obou Pico nainstaluj CircuitPython pro Raspberry Pi Pico. Z CircuitPython
Library Bundle zkopíruj `adafruit_hid` do složky `CIRCUITPY/lib/`.

1. Zkopíruj [code.py](../../Pico/RacingController/code.py) na kořen jednotky
   `CIRCUITPY` každého Pico.
2. Na Pico hráče 1 zkopíruj obsah souboru
   [player1.txt](../../Pico/RacingController/player1.txt) do nového souboru
   `player.txt` na `CIRCUITPY`.
3. Na Pico hráče 2 obdobně použij
   [player2.txt](../../Pico/RacingController/player2.txt), také pojmenovaný
   `player.txt`.
4. Při restartu nech joystick asi 320 ms uprostřed, aby se zkalibroval.

Pico hráče 1 posílá klávesy WASD, hráče 2 šipky. Profily jsou tedy odlišné,
i když jsou oba ovladače připojené současně.

## Instalace a spuštění hry

V terminálu na Raspberry Pi:

```sh
sudo apt update
sudo apt install python3-pygame
python3 main.py
```

Spusť poslední příkaz z adresáře `RPi/RacingGame`. Hra se otevře přes celou
obrazovku s pohledem každého hráče vedle sebe. `Esc` nebo START hru pozastaví
a znovu spustí. Tlačítko BACK (nebo `R` u hráče 1) začne nový závod. Vyhrává
první hráč, který dokončí tři kola.

## Ovládání

| Akce | Hráč 1 | Hráč 2 |
| --- | --- | --- |
| Zatáčet | Joystick vlevo/vpravo nebo A/D | Joystick vlevo/vpravo nebo šipky |
| Plyn / brzda | Joystick nahoru/dolů nebo W/S | Joystick nahoru/dolů nebo šipky |
| Krátké zrychlení | A nebo levý Shift | A nebo pravý Shift |
| Drift | B nebo mezerník | B nebo pravý Alt |
| Použít sebrané zrychlení | X nebo E | X nebo pravý Ctrl |
| Nový závod | BACK nebo R | BACK nebo Backspace |

