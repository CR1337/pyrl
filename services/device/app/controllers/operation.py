import time
import logging
from services.device.app.controllers.system import SystemController

from services.device.app.model.program import Program
from ..util.exceptions import RLException
from .fuse import FuseController
from ..util.system_time import get_system_time
from ..model.config import Config

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
    SCHEDULED_TIME = None
    PROGRAM = None
    STATE = 'unloaded'

    @classmethod
    def _set_state(cls, value):
        logging.debug(f"set state to {value}")
        cls.STATE = value

    @lock_interaction
    @classmethod
    def set_program(cls, program):
        if cls.STATE == 'loaded':
            raise ProgramAlreadyLoaded()
        elif cls.STATE == 'scheduled':
            raise ProgramScheduled()
        elif cls.STATE == 'running':
            raise ProgramRunning()
        logging.info(
            f"set program to {program.name} with {len(program)} commands"
        )
        cls.PROGRAM = program
        cls._set_state('loaded')

    @lock_interaction
    @classmethod
    def delete_program(cls):
        if cls.STATE == 'unloaded':
            raise NoProgramLoaded
        elif cls.STATE == 'scheduled':
            raise ProgramScheduled()
        elif cls.STATE == 'running':
            raise ProgramRunning()
        logging.info("delete program")
        cls.PROGRAM = None
        cls._set_state('unloaded')

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
        logging.info("run program")
        cls.PROGRAM.run(callback=cls._program_callback)
        cls._set_state('running')

    @lock_interaction
    @classmethod
    def stop_program(cls):
        if cls.STATE != 'running':
            raise NoProgramRunning()
        logging.info("stop program")
        cls.PROGRAM.stop()

    @raise_on_lock
    @lock_interaction
    @classmethod
    def schedule_program(cls, schedule_time):
        if cls.STATE == 'unloaded':
            raise NoProgramLoaded
        elif cls.STATE == 'scheduled':
            raise ProgramScheduled()
        elif cls.STATE == 'running':
            raise ProgramRunning()
        logging.info(f"schedule program for {schedule_time}")
        cls.SCHEDULED_TIME = schedule_time
        cls.SCHEDULE_THREAD = Thread(
            target=cls._schedule_handler,
            name="schedule_handler_thread"
        )
        cls.SCHEDULE_THREAD.start()
        cls._set_state('scheduled')

    @lock_interaction
    @classmethod
    def unschedule_program(cls):
        if cls.STATE != 'scheduled':
            raise NoProgramScheduled()
        logging.info('unschedule program')
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
        logging.info(f"fire {address}")
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
        logging.info("run testloop")
        cls.PROGRAM = Program.testloop_program()
        cls.PROGRAM.run(callback=cls._program_callback)
        cls._set_state('running')

    @classmethod
    def _program_callback(cls):
        logging.debug("running program callback")
        cls.PROGRAM = None
        cls._set_state('unloaded')

    @classmethod
    def _schedule_handler(cls):
        try:
            while not cls.UNSCHEDULE_EVENT.is_set():
                if cls.SCHEDULED_TIME <= get_system_time():
                    cls.PROGRAM.run(callback=cls._program_callback)
                    cls.STATE = 'running'
                    if cls.UNSCHEDULE_EVENT.is_set():
                        cls.UNSCHEDULE_EVENT.clear()
                    cls.SCHEDULED_TIME = None
                    return
                time.sleep(Config.SCHEDULING_RESOLUTION)
        except Exception:
            logging.exception("unexpected error in schedule handler")
            SystemController.put_asnyc_exception()

        if cls.UNSCHEDULE_EVENT.is_set():
            cls.UNSCHEDULE_EVENT.clear()
        cls.SCHEDULED_TIME = None
        cls.STATE = 'loaded'

    @classmethod
    def get_status(cls):
        return {
            'fuse_status': FuseController.get_status(),
            'program': None if cls.PROGRAM is None else cls.PROGRAM.as_dict(),
            'state': cls.STATE,
            'scheduled_time': cls.SCHEDULED_TIME.isostring()
        }
