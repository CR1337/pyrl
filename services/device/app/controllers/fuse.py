from threading import Lock
from functools import wraps


def lock_bus(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        FuseController.LOCK.acquire(blocking=True)
        result = func(*args, **kwargs)
        FuseController.LOCK.release()
        return result
    return wrapper


class FuseController():

    LOCK = Lock()

    @classmethod
    @lock_bus
    def light(cls, address):
        ...

    @classmethod
    @lock_bus
    def unlight(cls, address):
        ...

    @classmethod
    @lock_bus
    def lock(cls):
        ...

    @classmethod
    @lock_bus
    def unlock(cls, address):
        ...

    @classmethod
    @lock_bus
    def get_errors(cls):
        ...

    @classmethod
    def get_status(cls):
        return None
