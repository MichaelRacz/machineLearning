from test.test_log_backend import TestLogBackend
from svc.app.endpoint import flask_app

def before_all(context):
    context.test_log_backend = TestLogBackend(
        flask_app.config['ENVIRONMENT'],
        flask_app.config['KAFKA_HOSTS'],
        flask_app.config['WINE_TOPIC'])

def after_all(context):
    context.test_log_backend.tear_down()
