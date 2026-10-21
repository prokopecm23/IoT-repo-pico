import network
import time


SSID = "Pico-Hotspot"
PASSWORD = "Pico1234"


sta_interface = (
	network.WLAN.IF_STA if hasattr(network.WLAN, "IF_STA") else network.STA_IF
)
wifi = network.WLAN(sta_interface)
wifi.active(True)
time.sleep(1)
print("Hledam hotspot:", SSID)
matching_networks = []
for item in wifi.scan():
	scanned_ssid = item[0]
	if isinstance(scanned_ssid, bytes):
		scanned_ssid = scanned_ssid.decode()
	print("Nalezena sit:", scanned_ssid, "kanal:", item[2])
	if scanned_ssid == SSID:
		matching_networks.append(item)
if matching_networks:
	print("Hotspot nalezen, kanal:", matching_networks[0][2])
else:
	print("Hotspot v dosahu nenalezen.")

wifi.connect(SSID, PASSWORD)

for attempt in range(30):
	if wifi.isconnected():
		break
	print("Cekam na pripojeni...", attempt + 1)
	time.sleep(0.5)

if wifi.isconnected():
	print("Pripojeno k siti:", SSID)
	print("IP adresa:", wifi.ifconfig()[0])
else:
	print("Pripojeni se nezdarilo. Zkontrolujte hotspot a heslo.")
	status = wifi.status()
	print("Stav Wi-Fi:", status)
	if status == getattr(network, "STAT_WRONG_PASSWORD", None):
		print("Heslo je spatne.")
	elif status == getattr(network, "STAT_NO_AP_FOUND", None):
		print("Pico hotspot nenaslo.")
	elif status == getattr(network, "STAT_CONNECT_FAIL", None):
		print("Hotspot pripojeni odmitl nebo spojeni selhalo.")