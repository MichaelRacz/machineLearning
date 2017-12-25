import common.app.wine_db as database
from app.api.restplus import flask_app, api
from app.api.wines_endpoint import wines_ns, wines_circuit_breaker
from svc.app.endpoint import svc_ns, svc_circuit_breaker
from app.api.nearest_neighbor_classification_endpoint import nearest_neighbor_ns, nearest_neighbor_circuit_breaker
from test.test_log_backend import TestLogBackend
from features.steps.step_utilities import clear_database
from app.wine_domain import wines

def before_all(context):
    database.initialize()
    api.add_namespace(wines_ns)
    api.add_namespace(svc_ns)
    api.add_namespace(nearest_neighbor_ns)
    context.client = flask_app.test_client()
    context.wines_ns = '/v1/wines/'
    context.svc_ns = '/v1/wines/classification/svc/'
    context.nearest_neighbor_ns = '/v1/wines/classification/nearest_neighbor/'
    context.test_log_backend = TestLogBackend()
    context.test_log_backend.initialize()
    wines_circuit_breaker.open()
    svc_circuit_breaker.open()
    nearest_neighbor_circuit_breaker.open()
    wines.init()

def after_all(context):
    context.test_log_backend.tear_down()

def before_tag(context, tag):
    if tag == 'needs_state_reset':
        clear_database()
        context.test_log_backend.reset_topic()
    if tag == 'log_synchronization':
        pass
        #TODO: what should happen here

def after_tag(context, tag):
    if tag == 'log_synchronization':
        pass
        #TODO: what should happen here?
