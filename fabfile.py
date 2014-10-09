"""
You can see all commands with `$ fab -l`. Typical usages:
"""
import os
from fabric.api import local, run, env, put

RASPBERRY_PATH = "/home/pi/lights/"

# Change to fabfile directory, to make relative paths work
DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))
os.chdir(DIR_SCRIPT)

env.use_ssh_config = True

# Default hosts
if not env.hosts:
    env.hosts = ["ambipi"]


def upload():
    """ Upload python script to AmbiPi """
    put("src/*.py", RASPBERRY_PATH)

def start():
    run("python %sambipi.py -d start" % RASPBERRY_PATH)

def stop():
    run("python %sambipi.py -d stop" % RASPBERRY_PATH)

def restart():
    run("python %sambipi.py -d restart" % RASPBERRY_PATH)

