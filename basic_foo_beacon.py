#!/usr/bin/env python3

import sys
from time import sleep
from bleson import get_provider
from beacons import FooBeacon

try:
    adapter = get_provider().get_adapter()
    beacon = FooBeacon(adapter)
    beacon.data = b'\x02\x01\x06\x05\x22\x08\x06\x01'
    beacon.start()
    while True:
        sleep(10)

except KeyboardInterrupt:
    pass

finally:
    beacon.stop()
