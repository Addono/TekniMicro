# Enable WebREPL before everything else
import webrepl

webrepl.start()

import time
import esp

esp.osdebug(None)
import gc

gc.collect()

import network

# Disable acting as access point
ap = network.WLAN(network.AP_IF)
ap.active(False)
