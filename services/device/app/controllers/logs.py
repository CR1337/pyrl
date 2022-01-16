from ..util.system_time import get_system_time_isostring
from ..util.exceptions import RLException


class InvalidLogFormat(RLException):
    def __init__(self, log_format):
        self.log_format = log_format


class LogsController():

    LOGS_PATH = "/home/cr/pyrl"
    LOG_FILENAME = (
        f"{LOGS_PATH}/"
        f"{get_system_time_isostring()}_device.log"
    )
    LEVEL_COLORS = {
        'DEBUG': 'Aqua',
        'INFO': 'White',
        'WARNING': 'Gold',
        'ERROR': 'FireBrick',
        'CRITICAL': 'DeepPink'
    }

    @classmethod
    def initialize(cls):
        import logging
        logging.basicConfig(
            filename=cls.LOG_FILENAME,
            encoding='utf-8',
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s: %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        logging.debug("initialized logging system")
        logging.debug(f"now logging to {cls.LOG_FILENAME}")

    @classmethod
    def _log(cls, level, message):
        # logging interferes with flask. logging must not be imported
        # before app.run is called
        import logging
        {
            'debug': logging.debug,
            'info': logging.info,
            'warning': logging.warning,
            'error': logging.error,
            'exception': logging.exception,
            'critical': logging.critical
        }[level](message)

    @classmethod
    def debug(cls, message):
        cls._log('debug', message)

    @classmethod
    def info(cls, message):
        cls._log('info', message)

    @classmethod
    def warning(cls, message):
        cls._log('warning', message)

    @classmethod
    def error(cls, message):
        cls._log('error', message)

    @classmethod
    def exception(cls, message):
        cls._log('exception', message)

    @classmethod
    def critical(cls, message):
        cls._log('critial', message)

    @classmethod
    def _wrap_logs_in_html(cls, raw_logs):
        html_logs = ""
        for line in raw_logs:
            inside_traceback = not line[0].isnumeric()
            level = 'ERROR' if inside_traceback else line.split(":")[2][3:]
            line = line.replace(" ", "&nbsp;").replace("\n", "")
            line = f'<div style="color:{cls.LEVEL_COLORS[level]}">{line}</div>'
            line += "<br>"
            html_logs += f"{line}\n"
        return html_logs

    @classmethod
    def get_logs(cls, log_format):
        with open(cls.LOG_FILENAME, 'r') as file:
            raw_logs = file.read()
        if log_format == 'raw':
            return raw_logs
        elif log_format == 'html':
            return cls._wrap_logs_in_html(raw_logs)
        else:
            raise InvalidLogFormat(log_format)
