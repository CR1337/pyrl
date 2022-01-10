import time
from services.device.app.model.program import Program
from ..util.exceptions import RLException
from .fuse import FuseController
from ..model.timestamp import Timestamp

from threading import Lock, Event, Thread


class ProgramAlreadyLoaded(RLException):
    pass


class NoProgramLoaded(RLException):
    pass


class ProgramScheduled(RLException):
    pass


class NoProgramScheduled(RLException):
    pass


class ProgramRunning(RLException):
    pass


class NoProgramRunning(RLException):
    pass


class HardwareLocked(RLException):
    pass


def raise_on_lock(func):
    def wrapper(*args, **kwargs):
        if FuseController.is_locked():
            raise HardwareLocked()
        else:
            func(*args, **kwargs)
    return wrapper


def lock_interaction(func):
    def wrapper(*args, **kwargs):
        OperationController.LOCK.acquire(blocking=True)
        try:
            func(*args, **kwargs)
        finally:
            OperationController.LOCK.release()
    return wrapper


class OperationController():

    LOCK = Lock()
    UNSCHEDULE_EVENT = Event()
    SCHEDULE_THREAD = None
    PROGRAM = None
    STATE = 'unloaded'

    @lock_interaction
    @classmethod
    def set_program(cls, program):
        if cls.STATE == 'loaded':
            raise ProgramAlreadyLoaded()
        elif cls.STATE == 'scheduled':
            raise ProgramScheduled()
        elif cls.STATE == 'running':
            raise ProgramRunning()
        cls.PROGRAM = program
        cls.STATE = 'loaded'

    @lock_interaction
    @classmethod
    def delete_program(cls):
        if cls.STATE == 'unloaded':
            raise NoProgramLoaded
        elif cls.STATE == 'scheduled':
            raise ProgramScheduled()
        elif cls.STATE == 'running':
            raise ProgramRunning()
        cls.PROGRAM = None
        cls.STATE = 'unloaded'

    @raise_on_lock
    @lock_interaction
    @classmethod
    def run_program(cls):
        if cls.STATE == 'unloaded':
            raise NoProgramLoaded
        elif cls.STATE == 'scheduled':
            raise ProgramScheduled()
        elif cls.STATE == 'running':
            raise ProgramRunning()
        cls.PROGRAM.run(callback=cls._program_callback)
        cls.STATE = 'running'

    @lock_interaction
    @classmethod
    def stop_program(cls):
        if cls.STATE != 'running':
            raise NoProgramRunning()
        cls.PROGRAM.stop()

    @raise_on_lock
    @lock_interaction
    @classmethod
    def schedule_program(cls, timestamp):
        if cls.STATE == 'unloaded':
            raise NoProgramLoaded
        elif cls.STATE == 'scheduled':
            raise ProgramScheduled()
        elif cls.STATE == 'running':
            raise ProgramRunning()
        cls.SCHEDULE_THREAD = Thread(
            target=cls._schedule_handler,
            name="schedule_handler_thread",
            args=(timestamp,)
        )
        cls.SCHEDULE_THREAD.start()
        cls.STATE = 'scheduled'

    @lock_interaction
    @classmethod
    def unschedule_program(cls):
        if cls.STATE != 'scheduled':
            raise NoProgramScheduled()
        cls.UNSCHEDULE_EVENT.set()

    @raise_on_lock
    @lock_interaction
    @classmethod
    def fire(cls, address):
        if cls.STATE == 'loaded':
            raise ProgramAlreadyLoaded()
        elif cls.STATE == 'scheduled':
            raise ProgramScheduled()
        elif cls.STATE == 'running':
            raise ProgramRunning()
        FuseController.light(address)

    @raise_on_lock
    @lock_interaction
    @classmethod
    def testloop(cls):
        if cls.STATE == 'loaded':
            raise ProgramAlreadyLoaded()
        elif cls.STATE == 'scheduled':
            raise ProgramScheduled()
        elif cls.STATE == 'running':
            raise ProgramRunning()
        cls.PROGRAM = Program.testloop_program()
        cls.PROGRAM.run(callback=cls._program_callback)
        cls.STATE = 'running'

    @classmethod
    def _program_callback(cls):
        cls.PROGRAM = None
        cls.STATE = 'unloaded'

    @classmethod
    def _schedule_handler(cls, timestamp):
        while not cls.UNSCHEDULE_EVENT.is_set():
            if timestamp <= Timestamp.now():
                cls.PROGRAM.run(callback=cls._program_callback)
                cls.STATE = 'running'
                if cls.UNSCHEDULE_EVENT.is_set():
                    cls.UNSCHEDULE_EVENT.clear()
                return
            time.sleep(0.5)
        if cls.UNSCHEDULE_EVENT.is_set():
            cls.UNSCHEDULE_EVENT.clear()
        cls.STATE = 'loaded'

    @classmethod
    def get_status(cls):
        return None
