from threading import Thread
import threading
import time

import requests
from .operation import OperationController
from .system import SystemController
from ..model.config import Config


class HeartbeatController():

    THREAD = None
    STOP_EVENT = threading.Event()

    @classmethod
    def start(cls):
        cls.THREAD = Thread(
            target=cls._heartbeat_handler,
            name='heartbeat_handler_thread'
        )
        cls.THREAD.start()

    @classmethod
    def stop(cls):
        cls.STOP_EVENT.set()
        cls.THREAD.join()
        cls.THREAD = None
        cls.STOP_EVENT.clear()

    @classmethod
    def _heartbeat_handler(cls):
        while not cls.STOP_EVENT.is_set():
            heartbeat_data = {
                'operation_status': OperationController.get_status(),
                'system_status': SystemController.get_status(),
                'async_exceptions': SystemController.get_async_exceptions()
            }
            master_url = (
                f"http://{SystemController.get_connected_master_ip()}"
                f"/device-interface/heartbeat"
            )
            try:
                response = requests.post(
                    url=master_url,
                    json=heartbeat_data
                )
                response.raise_for_status()
            except requests.exceptions.RequestException:
                ...  # TODO: log
            time.sleep(Config.HEARTBEAT_INTERVAL)
