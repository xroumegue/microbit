#! /usr/bin/env python

from argparse import ArgumentParser
from os.path import realpath, exists
from subprocess import run, PIPE
from pathlib import Path
from time import sleep
import microfs as ufs
import sys
from struct import unpack, calcsize, iter_unpack

parser = ArgumentParser(description='Read and exploit CO2 data')

parser.add_argument(
        '--file',
        type=Path,
        help="Local data measurement file"
    )

args = parser.parse_args()

def copy_from_target(src):
    run(f"mpremote fs cp :{src} .".split(), stdout=PIPE)

def wait_until_connected():
    warn_once = True
    while True:
        ret = run('mpremote connect list'.split(), stdout=PIPE)
        if not ret.stdout:
            if warn_once:
                print("Connect the microbit to USB PC port")
                warn_once = False
                sleep(1)
        else:
            device=' '.join([a.decode() for a in ret.stdout.split()[3:]])
            print(f"Connected to {device}")
            break

if args.file:
    if exists(args.file):
        measFile = realpath(args.file)
    else:
        print("File {args.file} does not exist. Exiting!")
        sys.exit(1)
else:
    print("Downloading from target...")
    DEFAULT_MEAS_DATA_FILE='meas.dat'
    wait_until_connected()
    copy_from_target(DEFAULT_MEAS_DATA_FILE)
    measFile = realpath(DEFAULT_MEAS_DATA_FILE)

print(f"Using {measFile} as data measurement file")

def extract_data(fileName):
    data = []
    with open(fileName, 'rb') as f:
        rawData = f.read()
    reader = iter_unpack('H', rawData)
    data = [d[0] for d in reader]

    return data

data = extract_data(measFile)

#
# Placeholder for computing what you want with the data
#
def compute(d):
    from statistics import mean
    print(f"{len(d)} measurements have been saved with average value {mean(d)}")


compute(data)


