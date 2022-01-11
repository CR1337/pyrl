from flask import Blueprint, request, jsonify, render_template
from flask_api import status

from ..util.system_time import set_system_time

from .util import handle_exceptions
from ..controllers.system import SystemController
from ..controllers.logs import LogsController

system_blueprint = Blueprint('system_blueprint', __name__)


@system_blueprint.route(
    "/master",
    methods=['POST', 'DELETE'],
    endpoint='ep_master'
)
@handle_exceptions
def ep_master():
    if request.method == 'POST':
        master_ip = request.remote_addr
        SystemController.register_master(master_ip)
    elif request.method == 'DELETE':
        SystemController.deregister_master()
    return {}, status.HTTP_200_OK


@system_blueprint.route(
    "/system-time",
    methods=['POST'],
    endpoint='ep_system_time'
)
@handle_exceptions
def ep_system_time():
    data = request.get_json(force=True)
    set_system_time(data['system_time'])
    return {}, status.HTTP_200_OK


@system_blueprint.route(
    "/status",
    methods=['GET'],
    endpoint='ep_status'
)
def ep_status():
    return jsonify(SystemController.get_status()), status.HTTP_200_OK


@system_blueprint.route(
    "/logs",
    methods=['GET'],
    endpoint='ep_logs'
)
def ep_logs():
    return render_template(
        'logs.html',
        device_id=SystemController.get_device_id(),
        log_lines=LogsController.get_logs('html')
    ), status.HTTP_200_OK


@system_blueprint.route(
    "/logs/raw",
    methods=['GET'],
    endpoint='ep_logs_raw'
)
def ep_logs_raw():
    return LogsController.get_logs('raw'), status.HTTP_200_OK
