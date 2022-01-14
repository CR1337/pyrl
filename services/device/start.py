from app import register_blueprints
from os import environ
from flask import Flask


if __name__ == "__main__":
    app = Flask(__name__)

    @app.route("/", methods=['GET'], endpoint="route_index")
    def route_index():
        return "HELLO WORLD!!!"

    #register_blueprints(app)

    if bool(environ.get('PYRL_DEBUG', False)):
        app.run(
            host='0.0.0.0',
            port=80,
            debug=True,
            use_reloader=True,
            use_debugger=True,
            use_evalex=True,
            threaded=False,
        )
    else:
        app.run(
            host='0.0.0.0',
            port=80,
            debug=False,
            threaded=False,
            processes=4
        )
