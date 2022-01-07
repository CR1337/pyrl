import logging

from flask import Flask

from .endpoints.system import system_blueprint
from .endpoints.operation import operation_blueprint
from .endpoints.user_interface import user_iterface_blueprint

logging.basicConfig(
    filename="",  # TODO
    encoding='utf-8',
    level=logging.DEBUG,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = Flask(__name__)
app.register_blueprint(system_blueprint, url_prefix="/system")
app.register_blueprint(operation_blueprint, url_prefix="/operation")
app.register_blueprint(user_iterface_blueprint, url_prefix="/user-interface")
