#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import time
import math
import logging

from optparse import OptionParser
from random import randrange

import patterns
from daemon import Daemon
from LedStrip_WS2801 import LedStrip_WS2801

NUM_LEDS = 250

# Directory we look for media files
DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))

PIDFILE = os.path.join(DIR_SCRIPT, "ambipi.pid")
LOGFILE = os.path.join(DIR_SCRIPT, "ambipi.log")
LOGFORMAT = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"

# Setup Logging
logFormatter = logging.Formatter(LOGFORMAT)
rootLogger = logging.getLogger()

fileHandler = logging.FileHandler(LOGFILE)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

consoleHandler = logging.StreamHandler(sys.stdout)
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
rootLogger.setLevel(logging.DEBUG)

# Color Code
def rainbowAllWithBrighnessMover(ledStrip, times=10000):
    for t in range(0, times):
        for i in range(0, ledStrip.nLeds):
            ledStrip.setPixel(i, patterns.rainbow((1.1 * math.pi * (i + t)) / ledStrip.nLeds, (i + t) % 255))
        ledStrip.update()
        time.sleep(0.01)


# Main loop, either run from console or daemonized
def _main(options, args):
    rootLogger.info("ambipi: %s leds, options=%s, args=%s", NUM_LEDS, options, args)
    ledStrip = LedStrip_WS2801(NUM_LEDS)

    while True:
        (r, g, b) = (randrange(255), randrange(255), randrange(255))
        # patterns.knight_rider(ledStrip, 7, (r, g, b), 1, 0.01)
        # patterns.antialisedPoint(ledStrip, (r, g, b), step=0.7, dscale=0.1)

        # patterns.rainbowAll(ledStrip, 100, 0)
        rainbowAllWithBrighnessMover(ledStrip)

        # time.sleep(1)

        # patterns.fillAll(ledStrip, [0, 255, 0], delayTime)
        # patterns.rainbowAll(ledStrip, 200, 0.01)
        # patterns.fillAll(ledStrip, [255, 0, 0], 0.01)
        # patterns.fillAll(ledStrip, [0, 255, 0], 0.01)
        # patterns.fillAll(ledStrip, [0, 0, 255], 0.01)
        # patterns.antialisedPoint(ledStrip, [255, 0, 0], 0.5, 0.3)
        # patterns.antialisedPoint(ledStrip, [0, 255, 0], 0.5, 0.3)
        # patterns.antialisedPoint(ledStrip, [0, 0, 255], 0.5, 0.3)
        # patterns.rainbowAll(ledStrip, 500, 0.01)
        # patterns.knight_rider(ledStrip)


# Wrapper for main loop with exception logging
def main(options, args):
    try:
        _main(options, args)
    except:
        rootLogger.exception(sys.exc_info()[0])


# Simple Daemonization
class MyDaemon(Daemon):
    def __init__(self, pidfile, options, args):
        self.options = options
        self.args = args
        Daemon.__init__(self, pidfile)

    def run(self):
        main(self.options, self.args)


# Handle run from command line
if __name__ == "__main__":
    # Prepare help and options
    usage = """usage: %prog [options]"""
    desc = ("Bits Working AmbiPi")
    parser = OptionParser(usage=usage, description=desc)

    parser.add_option("-d", "--daemon", dest="daemon", action="store_true", help="Daemonize. -d [start|stop|restart]")
    parser.add_option("-v", "--version", dest="version", action="store_true", help="Show version")

    (options, args) = parser.parse_args()

    if options.version:
        print __version__
        exit(0)

    if options.daemon:
        daemon = MyDaemon(PIDFILE, options, args)
        if "start" == args[0]:
            daemon.start()

        elif "stop" == args[0]:
            daemon.stop()

        elif "restart" == args[0]:
            daemon.restart()

    else:
        main(options, args)
