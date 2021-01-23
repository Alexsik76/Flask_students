import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


def get_env_variable(name):
    try:
        return os.environ[name]
    except KeyError:
        message = f"Expected environment variable {name} not set."
        raise Exception(message)


DB_USER = get_env_variable("DB_USER")
DB_PW = get_env_variable("DB_PW")


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'dev'
    STATIC_FOLDER = 'app/static'
    TEMPLATES_FOLDER = 'app/templates'
    BASE_DIR = basedir
    # JSON_SORT_KEYS = False
    BOOTSTRAP_BOOTSWATCH_THEME = 'cosmo'
    # BOOTSTRAP_ICON_SIZE = '1.5em'
    # BOOTSTRAP_ICON_COLOR = 'light'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or f'postgresql://{DB_USER}{DB_PW}@localhost/{os.path.join(basedir, "app.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = True


class TestingConfig(Config):
    DEBUG = False
    TESTING = True


app_config = {
    'base_config': Config,
    'testing': TestingConfig,
    'develop': DevelopmentConfig
}
