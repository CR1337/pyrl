from flask import Blueprint, request, jsonify
from flask_api import status

from .util import handle_exceptions
from ..controllers.system import SystemController

system_blueprint = Blueprint('system_blueprint', __name__)


@system_blueprint.route(
    "/master",
    methods=['POST', 'DELETE'],
    endpoint='ep_master'
)
@handle_exceptions
def ep_master():
    if request.method == 'POST':
        ...
    elif request.method == 'DELETE':
        ...


@system_blueprint.route(
    "/system-time",
    methods=['POST'],
    endpoint='ep_system_time'
)
@handle_exceptions
def ep_system_time():
    ...


@system_blueprint.route(
    "/status",
    methods=['GET'],
    endpoint='ep_status'
)
def ep_status():
    return jsonify(SystemController.get_status())


@system_blueprint.route(
    "/logs",
    methods=['GET'],
    endpoint='ep_logs'
)
def ep_logs():
    ...
