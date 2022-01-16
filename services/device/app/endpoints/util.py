import sys
import traceback
from functools import wraps

from flask import make_response, request
from flask_api import status

from ..controllers.logs import LogsController
from ..util.exceptions import RLException


def log_request(message):
    LogsController.info(f"REQUEST from {request.remote_addr}: {message}")


def handle_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            exception_raised = False
        except RLException:
            status_code = status.HTTP_400_BAD_REQUEST
            LogsController.exception(msg="Bad Request")
            exception_raised = True
        except Exception:
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            LogsController.exception(msg="Internal Server Error")
            exception_raised = True
        finally:
            if exception_raised:
                exception_type, exception, trace_back = sys.exc_info()
                response_content = {
                    'exception_type': str(exception_type),
                    'excpetion_args': vars(exception),
                    'traceback': traceback.extract_tb(trace_back).format()
                }
                response = make_response((response_content, status_code))
            return response
    return wrapper
