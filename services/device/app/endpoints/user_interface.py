from flask import (Blueprint, Response, render_template, request,
                   send_from_directory)
from flask_api import status

import time
import json
from itertools import count

from .util import handle_exceptions
from ..model.config import Config
from ..controllers.operation import OperationController
from ..controllers.system import SystemController

user_iterface_blueprint = Blueprint('user_interface_blueprint', __name__)


@user_iterface_blueprint.route(
    "/",
    methods=['GET'],
    endpoint='ep_root'
)
@handle_exceptions
def ep_root():
    return render_template('user_interface.html')


@user_iterface_blueprint.route(
    "/status-stream",
    methods=['GET'],
    endpoint='ep_status_stream'
)
def ep_status_stream():
    def status_stream():
        for i in count(start=0):
            time.sleep(Config.STATUS_STREAM_INTERVAL)
            data = {
                'system_status': SystemController.get_status(),
                'operation_status': OperationController.get_status()
            }
            yield f"data: {json.dumps(data)}\nid: {str(i)}\n\n"
    return Response(
        status_stream(),
        mimetype="text/event-stream"
    )


@user_iterface_blueprint.route(
    "/static/<path:path>",
    methods=['GET'],
    endpoint='ep_static'
)
@handle_exceptions
def ep_static(path):
    return send_from_directory('static', path)
