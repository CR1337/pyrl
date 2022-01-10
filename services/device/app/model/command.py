from ..controllers.system import SystemController
from ..controllers.fuse import FuseController

from .address import Address
from .timestamp import Timestamp
from .config import Config

from threading import Thread
import time


class ForeignDeviceId(Exception):
    pass


class Command():

    def __init__(
        self, device_id, address_string, h, m, s, ds, name, description
    ):
        if device_id != SystemController.get_device_id():
            raise ForeignDeviceId()
        else:
            self._device_id = device_id

        self._address = Address(address_string)
        self._timestamp = Timestamp(h, m, s, ds)
        self._name = name
        self._description = description

    @property
    def timestamp(self):
        return self._timestamp

    def stage_fuse(self):
        FuseController.set_fuse_state(self._address, 'staged')

    def execute(self):
        execution_thread = Thread(
            target=self._execution_handler,
            name=f"command_execution_thread_{str(self._address)}"
        )
        execution_thread.start()

    def _execution_handler(self):
        try:
            FuseController.light(self._address)
            time.sleep(Config.FIRE_DURATION)
        finally:
            FuseController.set_fuse_state(self._address, 'fired')
            FuseController.unlight(self._address)
