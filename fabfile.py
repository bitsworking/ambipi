"""
You can see all commands with `$ fab -l`. Typical usages:
"""
import os
from fabric.api import local, run, env, put

# Change to fabfile directory, to make relative paths work
DIR_SCRIPT = os.path.dirname(os.path.realpath(__file__))
os.chdir(DIR_SCRIPT)

env.use_ssh_config = True

# Default hosts
if not env.hosts:
    env.hosts = ["ambipi"]


def upload():
    """ Upload python script to AmbiPi """
    put("src/*.py", "/home/pi/lights/")


def start():
    run("python /home/pi/lights/demo.py &")

def stop():
    run("killall python")
# def reboot():
#     run("sudo reboot")

# def shutdown():
#     run("sudo shutdown -h now")