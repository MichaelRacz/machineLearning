from flask import request
from flask_restplus import Resource, reqparse
from app.api.restplus import api
from app.api.model import initialize as initialize_web_model
import app.wine_domain.crud as wine_crud
from app.wine_domain.crud import UnknownRecordError
from app.wine_domain.distributed_log import DistributedLogContext
from app.api.logger import logger
import uuid
from datetime import datetime
from threading import Lock

def _handle_errors(function_name):
    def _handle_errors_decorator(f):
        def error_handling_f(*args, **kwargs):
            request_id = uuid.uuid4().hex
            try:
                logger.info("{} begin call '{}', request id: {}".format(str(datetime.now()), function_name, request_id))
                result = f(*args, **kwargs)
                logger.info("{} end call '{}', request id: {}".format(str(datetime.now()), function_name, request_id))
                return result
            except Exception as error:
                logger.error("{} failed call '{}', request id: {}, error message: {}"
                    .format(str(datetime.now()), function_name, request_id, str(error)))
                status_code = 404 if type(error) is UnknownRecordError else 500
                return {'error_message': str(error)}, status_code
        return error_handling_f
    return _handle_errors_decorator

class CircuitBreaker:
    def __init__(self, max_requests):
        self.max_requests = max_requests
        self.open_requests = 0
        self.is_open = True
        self.lock = Lock()

    def close(self, reason, status_code):
        self.lock.acquire()
        try:
            self.is_open = False
            self.reason = reason
            self.status_code = status_code
        finally:
            self.lock.release()

    def decorate(self, f):
        def decorated_f(*args, **kwargs):
            can_execute = False
            self.lock.acquire()
            try:
                can_execute = self.is_open and self.open_requests < self.max_requests
                if can_execute:
                    self.open_requests += 1
            finally:
                self.lock.release()
            if can_execute:
                try:
                    return f(*args, **kwargs)
                finally:
                    self.lock.acquire()
                    try:
                        self.open_requests -= 1
                    finally:
                        self.lock.release()
            else:
                if self.is_open is False :
                    return {'error_message': self.reason}, self.status_code
                else:
                    return {'error_message': 'Too many requests.'}, 429
        return decorated_f

wines_ns = api.namespace('wines', description='API of wine datastore')
web_model = initialize_web_model(api)

get_wine_arguments = reqparse.RequestParser()
get_wine_arguments.add_argument('id', type=int, location='args', required=True, nullable=False)

delete_wine_arguments = reqparse.RequestParser()
delete_wine_arguments.add_argument('id', type=int, location='args', required=True, nullable=False)

@wines_ns.route('/')
class Wines(Resource):
    @api.doc(
        description='This endpoint returns information of a wine record of a given id. The result indcludes all properties of the wine and its category.',
        id='get_wine',
        tags='Wines')
    @api.expect(get_wine_arguments, validate=True)
    @api.response(200, 'Wine successfully returned.', web_model.classified_wine)
    @api.response(404, 'Unknown id.', web_model.error)
    @api.response(500, 'Unexpected server error.', web_model.error)
    @_handle_errors('foo')
    def get(self):
        """
        Retrieve wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        wine = wine_crud.retrieve(id)
        classified_wine = _create_classified_wine(wine)
        return classified_wine, 200

    @api.doc(
        description='This endpoint deletes a wine record of a given id.',
        id='delete_wine',
        tags='Wines')
    @api.expect(delete_wine_arguments, validate=True)
    @api.response(204, 'Wine successfully deleted.')
    @api.response(404, 'Unknown id.', web_model.error)
    @api.response(500, 'Unexpected server error.', web_model.error)
    @_handle_errors('foo')
    def delete(self):
        """
        Delete wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        wine_crud.delete(id, DistributedLogContext.get_log())
        return {}, 204

    @api.doc(
        description='This endpoint creates a wine record with a correspondening class.',
        id='create_wine',
        tags='Wines')
    @api.expect(web_model.classified_wine, validate=True)
    @api.response(201, 'Wine successfully created.', web_model.wine_id)
    @api.response(500, 'Unexpected server error.', web_model.error)
    @_handle_errors('foo')
    def post(self):
        """
        Create wine
        """
        classified_wine = request.get_json(force=True)
        id = wine_crud.create(classified_wine, DistributedLogContext.get_log())
        return {'id': id}, 201

def _create_classified_wine(wine):
    wine_web = { \
        'alcohol': wine.alcohol, \
        'malic_acid': wine.malic_acid,
        'ash': wine.ash,
        'alcalinity_of_ash': wine.alcalinity_of_ash,
        'magnesium': wine.magnesium,
        'total_phenols': wine.total_phenols,
        'flavanoids': wine.flavanoids,
        'nonflavanoid_phenols': wine.nonflavanoid_phenols,
        'proanthocyanins': wine.proanthocyanins,
        'color_intensity': wine.color_intensity,
        'hue': wine.hue,
        'odxxx_of_diluted_wines': wine.odxxx_of_diluted_wines,
        'proline': wine.proline}
    return {'wine_class': wine.wine_class, 'wine': wine_web}
