from flask import Blueprint, request
from flask_api import status


system_blueprint = Blueprint('system_blueprint', __name__)


@system_blueprint.route(
    "/master",
    methods=['POST', 'DELETE'],
    endpoint='ep_master'
)
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
def ep_system_time():
    ...
