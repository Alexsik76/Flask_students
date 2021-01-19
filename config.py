from os import path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'dev'
    BASE_DIR = path.abspath(path.dirname(__file__))
    STATIC_FOLDER = 'app/static'
    TEMPLATES_FOLDER = 'app/templates'
    JSON_SORT_KEYS = False
    FILE_NAMES = ('abbreviations.txt', 'start.log', 'end.log')
    FIELDS = ('Position', 'Abbreviation', 'Name', 'Team', 'Start time', 'Finish time', 'Race time')
    BOOTSTRAP_BOOTSWATCH_THEME = 'cosmo'
    # BOOTSTRAP_ICON_SIZE = '1.5em'
    # BOOTSTRAP_ICON_COLOR = 'light'
    DATABASE = 'sqlite:///' + path.join(BASE_DIR, 'app.db')
    SWAGGER = {'title': 'REST API report of Monaco 2018 Racing',
               'uiversion': 3,
               'openapi': '3.0.2',
               'version': '0.0.3',
               'hide_top_bar': True,
               'favicon': "url_for('static', filename='image/favicon.png')"
               }


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
