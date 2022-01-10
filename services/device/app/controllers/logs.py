from ..util.system_time import get_system_time_isostring
import logging


class LogsController():

    LOGS_PATH = "/var/log/rl"
    LOG_FILENAME = (
        f"{LOGS_PATH}/"
        f"{get_system_time_isostring()}_device.log"
    )
    logging.basicConfig(
        filename=LOG_FILENAME,
        encoding='utf-8',
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s: %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    @classmethod
    def get_logs(cls):
        with open(cls.LOG_FILENAME, 'r') as file:
            return file.read()
