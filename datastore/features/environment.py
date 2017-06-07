import app.wine_domain.model as domain_model
from app.api.restplus import flask_app, api
from app.api.wines_endpoint import wines_ns
from test.test_log_backend import TestLogBackend

def before_all(context):
    domain_model.initialize()
    api.add_namespace(wines_ns)
    context.client = flask_app.test_client()
    context.wines_ns = '/v1/wines/'
    context.test_log_backend = TestLogBackend()
    context.test_log_backend.initialize()

def after_all(context):
    context.test_log_backend.tear_down()
