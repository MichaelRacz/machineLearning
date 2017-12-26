from flask import Flask, request
from flask_restplus import Api
from wines.app import database
from wines.app.endpoint import wines_ns, wines_circuit_breaker
from svc.app.endpoint import svc_ns, svc_circuit_breaker
from nearest_neighbor.app.endpoint import nearest_neighbor_ns, nearest_neighbor_circuit_breaker
from test.test_log_backend import TestLogBackend
from features.steps.step_utilities import clear_database
from wines.app import datastore

flask_app = Flask('Test app')
flask_app.config.from_envvar('CONFIG_FILE')

api = Api(flask_app,
    title='Test API',
    description='Test API.',
    version='1.0.0',
    prefix='/test',
    default_mediatype='application/json')

def before_all(context):
    database.initialize()
    api.add_namespace(wines_ns)
    api.add_namespace(svc_ns)
    api.add_namespace(nearest_neighbor_ns)
    context.client = flask_app.test_client()
    context.wines_ns = '/test/wines/'
    context.svc_ns = '/test/wines/classification/svc/'
    context.nearest_neighbor_ns = '/test/wines/classification/nearest_neighbor/'

    context.test_log_backend = TestLogBackend(
        flask_app.config['ENVIRONMENT'],
        flask_app.config['KAFKA_HOSTS'],
        flask_app.config['WINE_TOPIC'])

    wines_circuit_breaker.open()
    svc_circuit_breaker.open()
    nearest_neighbor_circuit_breaker.open()
    datastore.init(flask_app.config['KAFKA_HOSTS'], flask_app.config['WINE_TOPIC'])

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
