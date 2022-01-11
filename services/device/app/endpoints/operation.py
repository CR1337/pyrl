from dateutil import parser
from flask import Blueprint, jsonify, request
from flask_api import status

from ..controllers.fuse import FuseController
from ..controllers.operation import OperationController
from ..model.address import Address
from ..model.program import Program
from ..util.exceptions import RLException
from .util import handle_exceptions, log_request


class InvalidProgramControlAction(RLException):
    def __init__(self, action):
        self.action = action


operation_blueprint = Blueprint('operation_blueprint', __name__)


@operation_blueprint.route(
    "/program",
    methods=['POST', 'DELETE'],
    endpoint='ep_program'
)
@handle_exceptions
def ep_program():
    """Endpoint to set or delete a program.
    The POST body contains json data in the following form:
    {
        'program_name': 'STRING',
        'command_list': [
            {
                'device_id': 'STRING',
                'address': 'STRING',
                'h': INTEGER,
                'm': INTEGER,
                's': INTEGER,
                'ds': INTEGER,
                'name': 'STRING',
                'description' 'STRING'
            },
            ...
        ]
    }
    """
    if request.method == 'POST':
        data = request.get_json(force=True)
        command_list = data['command_list']
        program_name = data['program_name']
        log_request(
            f"set program {program_name} with {len(command_list)} commands"
        )
        program = Program(data['command_list'], data['program_name'])
        OperationController.set_program(program)
    elif request.method == 'DELETE':
        log_request("delete program")
        OperationController.delete_program()
    return {}, status.HTTP_200_OK


@operation_blueprint.route(
    "/program/control",
    methods=['POST'],
    endpoint='ep_program_control'
)
@handle_exceptions
def ep_program_control():
    data = request.get_json(force=True)
    action = data['action']
    if action == 'schedule':
        log_request(
            f"program control action: {action} "
            f"with time: {data['schedule_time']}"
        )
    else:
        log_request(f"program control action: {action}")

    if action == 'run':
        OperationController.run_program()
    elif action == 'stop':
        OperationController.stop_program()
    elif action == 'schedule':
        schedule_time_isostring = data['schedule_time']
        schedule_time = parser.parse(schedule_time_isostring)
        OperationController.schedule_program(schedule_time)
    elif action == 'unschedule':
        OperationController.unschedule_program()
    else:
        raise InvalidProgramControlAction(action)
    return {}, status.HTTP_200_OK


@operation_blueprint.route(
    "/fire",
    methods=['POST'],
    endpoint='ep_fire'
)
@handle_exceptions
def ep_fire():
    data = request.get_json(force=True)
    address = Address(data['address'])
    log_request(f"fire {address}")
    OperationController.fire(address)
    return {}, status.HTTP_200_OK


@operation_blueprint.route(
    "/lock",
    methods=['POST'],
    endpoint='ep_lock'
)
@handle_exceptions
def ep_lock():
    data = request.get_json(force=True)
    if data['lock_state']:
        log_request("lock")
        FuseController.lock()
    else:
        log_request("unlock")
        FuseController.unlock()
    return {}, status.HTTP_200_OK


@operation_blueprint.route(
    "/testloop",
    methods=['POST'],
    endpoint='ep_testloop'
)
@handle_exceptions
def ep_testloop():
    log_request("testloop")
    OperationController.testloop()
    return {}, status.HTTP_200_OK


@operation_blueprint.route(
    "/status",
    methods=['GET'],
    endpoint='ep_status'
)
def ep_status():
    log_request("get operation status")
    return jsonify(OperationController.get_status()), status.HTTP_200_OK
