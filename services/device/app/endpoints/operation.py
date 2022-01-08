from flask import Blueprint, request, jsonify
from flask_api import status

from .util import handle_exceptions
from ..controllers.operation import OperationController

operation_blueprint = Blueprint('operation_blueprint', __name__)


@operation_blueprint.route(
    "/program",
    methods=['POST', 'DELETE'],
    endpoint='ep_program'
)
@handle_exceptions
def ep_program():
    if request.method == 'POST':
        ...
    elif request.method == 'DELETE':
        ...


@operation_blueprint.route(
    "/program/control",
    methods=['POST'],
    endpoint='ep_program_control'
)
@handle_exceptions
def ep_program_control():
    ...


@operation_blueprint.route(
    "/fire",
    methods=['POST'],
    endpoint='ep_fire'
)
@handle_exceptions
def ep_fire():
    ...


@operation_blueprint.route(
    "/lock",
    methods=['POST'],
    endpoint='ep_lock'
)
@handle_exceptions
def ep_lock():
    ...


@operation_blueprint.route(
    "/testloop",
    methods=['POST'],
    endpoint='ep_testloop'
)
@handle_exceptions
def ep_testloop():
    ...


@operation_blueprint.route(
    "/status",
    methods=['GET'],
    endpoint='ep_status'
)
def ep_status():
    return jsonify(OperationController.get_status())
