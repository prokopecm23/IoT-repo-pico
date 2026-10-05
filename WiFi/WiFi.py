import network


SSID = "Pico-Hotspot"
PASSWORD = "PicoWifi123"


def start_hotspot():
	ap_interface = (
		network.WLAN.IF_AP if hasattr(network.WLAN, "IF_AP") else network.AP_IF
	)
	access_point = network.WLAN(ap_interface)
	access_point.config(ssid=SSID, key=PASSWORD, security=3)
	access_point.active(True)

	while not access_point.active():
		pass

	print("Hotspot je zapnuty.")
	print("Sit:", SSID)
	print("Heslo:", PASSWORD)
	print("Adresa:", access_point.ifconfig()[0])
	print("Hotspot poskytuje lokalni sit, ne pripojeni k internetu.")
	return access_point


ap = start_hotspot()
