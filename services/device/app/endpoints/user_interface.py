from flask import (Blueprint, Response, render_template, request,
                   send_from_directory)
from flask_api import status

import time
import json
from itertools import count

from .util import handle_exceptions

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
            time.sleep(0.5)
            # TODO:
            data = {
                'system_status': {
                    'system_time': None,
                    'connected_master_ip': None
                },
                'operation_status': {
                    'loaded_program': None,
                    'program_state': None,
                    'fuse_states': [None],
                    'locked': None
                }
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
