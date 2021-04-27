import pytest
from app import create_app, create_db


@pytest.fixture(scope='session')
def client():
    flask_app = create_app(test_config=True)

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            create_db.init_db()
            yield testing_client


# @pytest.fixture
# def runner(app):
#
#     return app.test_cli_runner()
