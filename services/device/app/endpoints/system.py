from flask import Blueprint, jsonify, render_template, request
from flask_api import status

from ..controllers.logs import LogsController
from ..controllers.system import SystemController
from ..util.system_time import set_system_time
from .util import handle_exceptions, log_request

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
        log_request("master registration")
        SystemController.register_master(master_ip)
    elif request.method == 'DELETE':
        log_request("master deregistration")
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
    system_time_isostring = data['system_time']
    log_request(f"set system time to {system_time_isostring}")
    set_system_time(system_time_isostring)
    return {}, status.HTTP_200_OK


@system_blueprint.route(
    "/status",
    methods=['GET'],
    endpoint='ep_status'
)
def ep_status():
    log_request("get system status")
    return jsonify(SystemController.get_status()), status.HTTP_200_OK


@system_blueprint.route(
    "/logs",
    methods=['GET'],
    endpoint='ep_logs'
)
def ep_logs():
    log_request("REQEST: get html logs")
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
    log_request("get raw logs")
    return LogsController.get_logs('raw'), status.HTTP_200_OK
