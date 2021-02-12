#!/usr/bin/env python3

import sys
from time import sleep
from bleson import get_provider
from beacons import FooBeacon

try:
    adapter = get_provider().get_adapter()
    beacon = FooBeacon(adapter)
    beacon.url = 'https://narwo.dev/'
    beacon.start()
    while True:
        sleep(10)

except KeyboardInterrupt:
    pass

finally:
    beacon.stop()
