from ..util.system_time import get_system_time_isostring
import logging
from ..util.exceptions import RLException


class InvalidLogFormat(RLException):
    def __init__(self, log_format):
        self.log_format = log_format


class LogsController():

    LOGS_PATH = "/var/log/pyrl"
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

    LEVEL_COLORS = {
        'DEBUG': 'Aqua',
        'INFO': 'White',
        'WARNING': 'Gold',
        'ERROR': 'FireBrick',
        'CRITICAL': 'DeepPink'
    }

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