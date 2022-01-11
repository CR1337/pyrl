from .controllers.logs import LogsController

from flask import Flask

from .endpoints.system import system_blueprint
from .endpoints.operation import operation_blueprint
from .endpoints.user_interface import user_iterface_blueprint


app = Flask(__name__)
app.register_blueprint(system_blueprint, url_prefix="/system")
app.register_blueprint(operation_blueprint, url_prefix="/operation")
app.register_blueprint(user_iterface_blueprint, url_prefix="/user-interface")
