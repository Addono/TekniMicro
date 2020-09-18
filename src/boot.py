# Enable WebREPL before everything else
import webrepl

webrepl.start()

import time
import esp

esp.osdebug(None)
import gc

gc.collect()
