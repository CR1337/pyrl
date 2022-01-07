import shlex
import subprocess
from datetime import datetime


def set_system_time(system_time):
    subprocess.call(shlex.split("timedatectl set-ntp false"))
    subprocess.call(shlex.split(f"sudo date -s '{system_time}'"))


def get_system_time():
    return datetime.now().replace(tzinfo=None).isoformat()
