import app.wine_domain.database as database
from app.api.restplus import flask_app, api
from app.api.wines_endpoint import wines_ns
from app.api.svc_classification_endpoint import svc_ns
from test.test_log_backend import TestLogBackend
from app.api.circuit_breaker import wines_circuit_breaker
from features.steps.step_utilities import clear_database
from app.wine_domain.distributed_log import DistributedLogContext

def before_all(context):
    database.initialize()
    api.add_namespace(wines_ns)
    api.add_namespace(svc_ns)
    context.client = flask_app.test_client()
    context.wines_ns = '/v1/wines/'
    context.svc_ns = '/v1/wines/classification/svc/'
    context.test_log_backend = TestLogBackend()
    context.test_log_backend.initialize()
    wines_circuit_breaker.open()

def after_all(context):
    context.test_log_backend.tear_down()

def before_tag(context, tag):
    if tag == 'needs_state_reset':
        clear_database()
        context.test_log_backend.reset_topic()
        DistributedLogContext.free_log()
