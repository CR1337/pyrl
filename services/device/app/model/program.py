from .command import Command, ForeignDeviceId

from threading import Thread, Event


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
        self._pause_event = Event()
        self._continue_event = Event()
        self._stop_event = Event()

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

    def run(self):
        self._thread.start()

    def pause(self):
        self._pause_event.set()

    def continue_(self):
        self._continue_event.set()

    def stop(self):
        self._stop_event.set()

    def _execution_handler(self):
        ...
