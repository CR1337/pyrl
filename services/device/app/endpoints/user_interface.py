from flask import Blueprint, request, render_template, send_from_directory
from flask_api import status

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
    "/static/<path:path>",
    methods=['GET'],
    endpoint='ep_static'
)
@handle_exceptions
def ep_static(path):
    return send_from_directory('static', path)
