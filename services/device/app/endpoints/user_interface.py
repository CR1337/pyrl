from flask import Blueprint, request
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
    ...
