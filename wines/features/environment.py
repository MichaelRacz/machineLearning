from test.test_log_backend import TestLogBackend
from wines.app.database import engine
import json
from wines.app import endpoint
from wines.app.endpoint import flask_app, InitializationScope

def before_all(context):
    context.test_log_backend = TestLogBackend(
        flask_app.config['ENVIRONMENT'],
        flask_app.config['KAFKA_HOSTS'],
        flask_app.config['WINE_TOPIC'])
    context.endpoint_scope = InitializationScope()
    context.endpoint_scope.__enter__()
    context.client = flask_app.test_client()
    context.wines_ns = '/v1/wines/'

def after_all(context):
    context.endpoint_scope.__exit__()
    context.test_log_backend.tear_down()

def before_tag(context, tag):
    if tag == 'needs_state_reset':
        _clear_database()
        context.test_log_backend.reset_topic()

def _clear_database():
    engine.execute('DELETE FROM Wines')
