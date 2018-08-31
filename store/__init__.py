import os
from flask import Flask
from flask_socketio import SocketIO
import eventlet


socketio = SocketIO()


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='mysql+mysqlconnector://root:root@db/store',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        REDIS_URL='redis://redis:6379/0',
        REDIS_QUEUES=['default'],
    )

    from store.models import db, migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Required for SocketIO to use Redis without requests hanging
    eventlet.monkey_patch()

    socketio.init_app(app, message_queue=app.config['REDIS_URL'])

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import api
    app.register_blueprint(api.bp)

    return app
