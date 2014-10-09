#!/usr/bin/env python
# encoding: utf-8
import os
import time
import shlex
import subprocess
from optparse import OptionParser
from random import randrange

from daemon import Daemon
import patterns
from LedStrip_WS2801 import LedStrip_WS2801

# Directory we look for media files
DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))

# PID
PIDFILE = os.path.join(DIR_SCRIPT, "ambipi.pid")


def main(options, args):
    print "ambipi lights, options=%s, args=%s" % (options, args)

    ledStrip = LedStrip_WS2801(250)
    # delayTime = 0.01

    while True:
        (r, g, b) = (randrange(255), randrange(255), randrange(255))
        # patterns.knight_rider(ledStrip, 7, (r, g, b), 1, 0.01)
        patterns.antialisedPoint(ledStrip, (r, g, b), 1, 0.1)
        # patterns.rainbowAll(ledStrip, 250, 0)

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


class MyDaemon(Daemon):
    def __init__(self, pidfile, options, args):
        self.options = options
        self.args = args
        Daemon.__init__(self, pidfile)

    def run(self):
        main(self.options, self.args)


if __name__ == "__main__":
    # Prepare help and options
    usage = """usage: %prog [options] (start|stop|restart)"""
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
