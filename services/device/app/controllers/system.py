from ..util.system_time import get_system_time, set_system_time
from ..util.exceptions import RLException


class MasterAlreadyRegistered(RLException):
    pass


class NoMasterRegistered(RLException):
    pass


class SystemController():

    _connected_master_ip = None

    @classmethod
    def change_system_time(cls, system_time):
        set_system_time(system_time)

    @classmethod
    def register_master(cls, master_ip):
        if cls._connected_master_ip is not None:
            raise MasterAlreadyRegistered()
        cls._connected_master_ip = master_ip

    @classmethod
    def deregister_master(cls):
        if cls._connected_master_ip is None:
            raise NoMasterRegistered()
        cls._connected_master_ip = None

    @classmethod
    def get_status(cls):
        return {
            'system_time': get_system_time(),
            'connected_master_ip': cls._connected_master_ip
        }

    @classmethod
    def get_connected_master_ip(cls):
        return cls._connected_master_ip

    @classmethod
    def get_device_id(cls):
        return ""  # TODO