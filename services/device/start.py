from app import app
from os import environ

from .app.controllers.logs import LogsController


if __name__ == "__main__":
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

    LogsController.initialize()
