import app.wine_domain.database as database
from app.api.restplus import flask_app, api
from app.api.wines_endpoint import wines_ns
from test.test_log_backend import TestLogBackend
from app.api.circuit_breaker import wines_circuit_breaker

def before_all(context):
    database.initialize()
    api.add_namespace(wines_ns)
    context.client = flask_app.test_client()
    context.wines_ns = '/v1/wines/'
    context.test_log_backend = TestLogBackend()
    context.test_log_backend.initialize()
    wines_circuit_breaker.open()

def after_all(context):
    context.test_log_backend.tear_down()
