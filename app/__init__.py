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


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config:
        app.config.from_object(app_config['testing'])
    else:
        app.config.from_object(app_config['develop'])
    csrf.init_app(app)
    bootstrap.init_app(app)



    db.init_app(app)
    from app.create_db import init_app
    init_app(app)

    ma.init_app(app)
    Markdown(app)
    from app.models import StudentModel
    from app.main.forms import StudentBaseForm

    with app.app_context():
        StudentBaseForm.get_choices()

    from app.api import bp_api
    app.register_blueprint(bp_api, url_prefix='/api/v1')

    from app.main import bp
    app.register_blueprint(bp)
    return app


from app import models
