import pywifi
from pywifi import const
import time


def scan_wifi():
    wifi = pywifi.PyWiFi()

    ifaces = wifi.interfaces()

    if not ifaces:
        return ["No Wi-Fi adapter found"]

    iface = ifaces[0]

    iface.scan()

    time.sleep(3)

    results = iface.scan_results()

    networks = []

    for network in results:
        if network.ssid:
            networks.append(network.ssid)

    return sorted(list(set(networks)))