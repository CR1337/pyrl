import sys
import traceback
from logging import exception
from os import environ
from queue import Queue

from ..util.exceptions import RLException
from ..util.system_time import get_system_time, set_system_time
from .logs import LogsController


class MasterAlreadyRegistered(RLException):
    pass


class NoMasterRegistered(RLException):
    pass


class SystemController():

    CONNECTED_MASTER_IP = None
    ASYNC_EXCEPTIONS = Queue()

    @classmethod
    def change_system_time(cls, system_time):
        LogsController.info(f"change system time to {system_time}")
        set_system_time(system_time)

    @classmethod
    def register_master(cls, master_ip):
        LogsController.info(f"register master: {master_ip}")
        if cls.CONNECTED_MASTER_IP is not None:
            raise MasterAlreadyRegistered()
        cls.CONNECTED_MASTER_IP = master_ip

    @classmethod
    def deregister_master(cls):
        LogsController.info("deregister master")
        if cls.CONNECTED_MASTER_IP is None:
            raise NoMasterRegistered()
        cls.CONNECTED_MASTER_IP = None

    @classmethod
    def put_asnyc_exception(cls):
        exception_type, exception, trace_back = sys.exc_info()
        cls.ASYNC_EXCEPTIONS.put({
            'exception_type': str(exception_type),
            'excpetion_args': vars(exception),
            'traceback': traceback.extract_tb(trace_back).format()
        })

    @classmethod
    def get_async_exceptions(cls):
        if cls.ASYNC_EXCEPTIONS.empty():
            return None
        exceptions = []
        while not cls.ASYNC_EXCEPTIONS.empty():
            exception.append(cls.ASYNC_EXCEPTIONS.get(block=False))
        return exceptions

    @classmethod
    def get_status(cls):
        return {
            'device_id': cls.get_device_id(),
            'system_time': get_system_time(),
            'connected_master_ip': cls.CONNECTED_MASTER_IP
        }

    @classmethod
    def get_connected_master_ip(cls):
        return cls.CONNECTED_MASTER_IP

    @classmethod
    def get_device_id(cls):
        return environ['PYRL_DEVCIE_ID']

    @classmethod
    def is_in_debug_mode(cls):
        return bool(environ.get('PYRL_DEBUG', False))
