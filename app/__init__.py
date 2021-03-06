from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flaskext.markdown import Markdown


bootstrap = Bootstrap()
db = SQLAlchemy()
ma = Marshmallow()
csrf = CSRFProtect()


def get_choices_v1(flask_app):
    """ Creates choices lists for Swaggers documentation.
    Lists of groups and courses must be created before the first api call for them to appear in the Swagger.
    But when running init-db, if the database does not exist, it causes an error.
    """
    from app.models import StudentModel
    if db.get_engine(flask_app).table_names():
        with flask_app.app_context():
            StudentModel.get_all_groups_and_courses()


def create_app(config='base_config'):
    app = Flask(__name__)
    app.config.from_object(app_config.get(config))
    csrf.init_app(app)
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    bootstrap.init_app(app)

    Markdown(app)

    db.init_app(app)

    from app.create_db import init_app
    init_app(app)

    ma.init_app(app)

    get_choices_v1(app)
    from app.api import bp_api
    app.register_blueprint(bp_api, url_prefix='/api/v1/')

    from app.main import bp
    app.register_blueprint(bp)

    return app


from app import models
