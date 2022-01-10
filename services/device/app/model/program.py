from subprocess import call
from services.device.app.model.timestamp import Timestamp
from .command import Command, ForeignDeviceId

from threading import Thread, Event
import time
from datetime import datetime


class Program():

    @classmethod
    def testloop_program(cls):
        ...  # TODO

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
        start_timestamp = Timestamp.now()
        command_idx = 0

        while (not self._stop_event.is_set()) and len(self._commands) > 0:
            command = self._commands[command_idx]
            current_relative_timestamp = Timestamp.now() - start_timestamp
            if command.timestamp <= current_relative_timestamp:
                command.execute()
                command_idx += 1
                if command_idx >= len(self._commands):
                    break
            time.sleep(0.05)

        if self._stop_event.is_set():
            self._stop_event.clear()
        self._callback()
        self._callback = None
