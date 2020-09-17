# Enable WebREPL before everything else
import webrepl

webrepl.start()

import time
import esp

esp.osdebug(None)
import gc

gc.collect()

from config import load_config

CONFIG = load_config()


def do_connect():
    import network

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect(CONFIG["WIFI_SSID"], CONFIG["WIFI_PASSWORD"])
        while not wlan.isconnected():
            pass
    print("network config:", wlan.ifconfig())


# Connect to the WiFi
do_connect()
