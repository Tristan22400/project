import os

import flask
import flask_cors

from . import auth
from . import db
from . import exams
from .entities.base import Base


def create_app(test_config=None):
    # creating the Flask application
    app = flask.Flask(__name__, instance_relative_config=True)
    flask_cors.CORS(app)

    # load configuration from config.py
    app.config.from_object('config')

    if test_config is None:
        # load the instance/config.py, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # if needed, generate database schema
    with app.app_context():
        Base.metadata.create_all(db.get_engine())

    app.register_blueprint(auth.blueprint)
    app.register_blueprint(exams.blueprint)

    return app
