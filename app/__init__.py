from flask import Flask
from config import app_config
from flask_sqlalchemy import SQLAlchemy, inspect
from flask_marshmallow import Marshmallow
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flaskext.markdown import Markdown


bootstrap = Bootstrap()
db = SQLAlchemy()
ma = Marshmallow()
csrf = CSRFProtect()


def create_app(test_config=False):
    app = Flask(__name__)
    if test_config:
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['develop'])

    csrf.init_app(app)
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    bootstrap.init_app(app)

    Markdown(app)

    db.init_app(app)

    from app.create_db import init_app
    init_app(app)

    ma.init_app(app)

    from app.models import StudentModel
    engine = db.get_engine(app)
    tables = engine.table_names()
    if tables:
        with app.app_context():
            StudentModel.get_all_groups_and_courses()

    from app.api import bp_api
    app.register_blueprint(bp_api, url_prefix='/api/v1/')

    from app.main import bp
    app.register_blueprint(bp)
    return app


from app import models
