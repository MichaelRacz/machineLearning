from flask import Flask
from flask_restplus import Api

flask_app = Flask(__name__)
flask_app.config.from_envvar('CONFIG_FILE')

api = Api(flask_app,
    title='Machine learning',
    description='Machine learning services.',
    version='1.0.0',
    prefix='/v1',
    default_mediatype='application/json')
