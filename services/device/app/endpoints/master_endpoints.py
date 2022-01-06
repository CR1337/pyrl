from flask import Blueprint, request

master_bp = Blueprint('master_bp', __name__)


@master_bp.route("/program", methods=['POST', 'DELETE'], endpoint='ep_program')
def ep_program():
    ...


@master_bp.route(
    "/program/control",
    methods=['POST'],
    endpoint='ep_program_control'
)
def ep_program_control():
    ...


@master_bp.route("/fire", methods=['POST'], endpoint='ep_fire')
def ep_fire():
    ...


@master_bp.route("/lock", methods=['GET', 'POST'], endpoint='ep_lock')
def ep_lock():
    ...
