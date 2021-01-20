import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'dev'
    STATIC_FOLDER = 'app/static'
    TEMPLATES_FOLDER = 'app/templates'
    # JSON_SORT_KEYS = False
    BOOTSTRAP_BOOTSWATCH_THEME = 'cosmo'
    # BOOTSTRAP_ICON_SIZE = '1.5em'
    # BOOTSTRAP_ICON_COLOR = 'light'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or f'postgresql://{user}{password}@localhost/{os.path.join(basedir, "app.db")}'


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
