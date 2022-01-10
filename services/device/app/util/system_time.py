import shlex
import subprocess
from datetime import datetime


def set_system_time(system_time):
    if isinstance(system_time, datetime):
        system_time = system_time.replace(tzinfo=None).isoformat()
    subprocess.call(shlex.split("timedatectl set-ntp false"))
    subprocess.call(shlex.split(f"sudo date -s '{system_time}'"))


def get_system_time():
    return datetime.now().replace(tzinfo=None)


def get_system_time_isostring():
    return get_system_time().isoformat()

