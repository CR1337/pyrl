from .timestamp import Timestamp
from .command import Command, ForeignDeviceId
from ..util.system_time import get_system_time
from .config import Config
from ..controllers.fuse import FuseController
from ..controllers.system import SystemController

from itertools import product
from threading import Thread, Event
import time
import logging


class Program():

    @classmethod
    def testloop_program(cls):
        letters = FuseController.CHIP_ADDRESSES.keys()
        timestamp_generator = Timestamp.evenly_spaced(
            16 * len(letters),
            Config.TESTLOOP_INTERVAL
        )
        command_list = []
        for letter, number in product(letters, range(16)):
            address_string = f"{letter}{number}"
            timestamp = next(timestamp_generator)
            command_list.append({
                'device_id': SystemController.get_device_id(),
                'address': address_string,
                'h': timestamp.h,
                'm': timestamp.m,
                's': timestamp.s,
                'ds': timestamp.ds,
                'name': f"testloop_{address_string}",
                'description': f"fires {address_string}"
            })
        return cls(command_list, 'testloop')

    def __init__(self, command_list, program_name):
        self._command_list = command_list
        self._program_name = program_name
        self._commands = []
        self._read_command_list()

        self._thread = Thread(
            target=self._execution_handler,
            name="program_execution_handler"
        )
        self._stop_event = Event()
        self._callback = None

    def _read_command_list(self):
        for command_dict in self._command_list:
            try:
                command = Command(**command_dict)
            except ForeignDeviceId:
                continue
            else:
                self._commands.append(command)

        self._commands = sorted(
            self._commands,
            key=lambda cmd: cmd.timestamp
        )

    def run(self, callback):
        self._callback = callback
        self._thread.start()

    def stop(self):
        self._stop_event.set()

    def _execution_handler(self):
        start_time = get_system_time()
        command_idx = 0

        while (not self._stop_event.is_set()) and len(self._commands) > 0:
            try:
                command = self._commands[command_idx]
                current_relative_timestamp = Timestamp.from_datetime_delta(
                    get_system_time(),
                    start_time
                )
                if command.timestamp <= current_relative_timestamp:
                    command.execute()
                    command_idx += 1
                    if command_idx >= len(self._commands):
                        break
            except Exception:
                logging.exception(
                    "unexpected error in program execution handler"
                )
                SystemController.put_asnyc_exception()
            time.sleep(Config.PROGRAM_RESOLUTION)

        if self._stop_event.is_set():
            self._stop_event.clear()
        self._callback()
        self._callback = None

    def __len__(self):
        return self._commands

    @property
    def name(self):
        return self._program_name

    @property
    def as_dict(self):
        return {
            'name': self._program_name,
            'commands': self._command_list
        }
