from .controllers.logs import LogsController

from .endpoints.system import system_blueprint
from .endpoints.operation import operation_blueprint
from .endpoints.user_interface import user_iterface_blueprint

# How to multifiles: https://explore-flask.readthedocs.io/en/latest/configuration.html


def register_blueprints(app):
    app.register_blueprint(system_blueprint, url_prefix="/system")
    app.register_blueprint(operation_blueprint, url_prefix="/operation")
    app.register_blueprint(user_iterface_blueprint, url_prefix="/user-interface")