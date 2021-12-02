#! /usr/bin/env python

import microfs as ufs
from os.path import realpath
from time import sleep

warn_once = True
while True:
    try:
        ubit = ufs.get_serial()
        break
    except IOError:
        if warn_once:
            print("Connect the microbit to USB PC port")
            warn_once = False
        sleep(1)

files = [
    "sgp30.py",
    "tm1637.py",
    "main.py",
]

for file in files:
    print(f"Uploading {file}")
    ufs.put(realpath(file), file, serial = ubit)


print(f"Press Microbit Reset button to reboot and test the Software...")
