import network  # type: ignore[import-not-found]


SSID = "Pico-Hotspot"
PASSWORD = "Pico1234"


def start_hotspot():
	ap_interface = (
		network.WLAN.IF_AP if hasattr(network.WLAN, "IF_AP") else network.AP_IF
	)
	access_point = network.WLAN(ap_interface)
	try:
		access_point.config(ssid=SSID, key=PASSWORD, security=3, channel=6)
	except (TypeError, ValueError):
		access_point.config(essid=SSID, password=PASSWORD, authmode=3, channel=6)
	access_point.active(True)

	print("Hotspot je zapnuty.")
	print("Sit:", SSID)
	print("Heslo:", PASSWORD)
	print("Adresa:", access_point.ifconfig()[0])
	print("Hotspot poskytuje lokalni sit, ne pripojeni k internetu.")
	return access_point


ap = start_hotspot()
