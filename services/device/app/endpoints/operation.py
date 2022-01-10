from flask import Blueprint, request, jsonify
from flask_api import status
from dateutil import parser

from .util import handle_exceptions
from ..model.program import Program
from ..model.address import Address
from ..controllers.operation import OperationController
from ..controllers.fuse import FuseController

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
        program = Program(data['command_list'], data['program_name'])
        OperationController.set_program(program)
    elif request.method == 'DELETE':
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
        ...  # TODO
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
        FuseController.lock()
    else:
        FuseController.unlock()
    return {}, status.HTTP_200_OK


@operation_blueprint.route(
    "/testloop",
    methods=['POST'],
    endpoint='ep_testloop'
)
@handle_exceptions
def ep_testloop():
    OperationController.testloop()
    return {}, status.HTTP_200_OK


@operation_blueprint.route(
    "/status",
    methods=['GET'],
    endpoint='ep_status'
)
def ep_status():
    return jsonify(OperationController.get_status()), status.HTTP_200_OK
