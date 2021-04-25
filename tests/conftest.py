import pytest
from app import create_app
from app.create_db import init_db


@pytest.fixture
def client():
    app = create_app()

    app.config["TESTING"] = True
    app.testing = True

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    client = app.test_client()
    with app.app_context():
        init_db()
    yield client


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
