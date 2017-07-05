from flask import request
from flask_restplus import Resource, reqparse
from app.api.restplus import api, web_model
import app.wine_domain.facade as wine_facade
from app.wine_domain.database import UnknownRecordError
from app.api.logger import logger
import uuid
from datetime import datetime
from werkzeug.exceptions import HTTPException
from app.api.circuit_breaker import wines_circuit_breaker

def _handle_errors(function_name):
    def _handle_errors_decorator(f):
        def error_handling_f(*args, **kwargs):
            request_id = uuid.uuid4().hex
            try:
                logger.info("{} begin call '{}', request id: {}".format(str(datetime.now()), function_name, request_id))
                result = f(*args, **kwargs)
                logger.info("{} end call '{}', request id: {}".format(str(datetime.now()), function_name, request_id))
                return result
            except HTTPException as error:
                logger.error("{} failed call '{}' (framework validation), request id: {}, error message: {}"
                    .format(str(datetime.now()), function_name, request_id, repr(error)))
                raise
            except Exception as error:
                logger.error("{} failed call '{}', request id: {}, error message: {}"
                    .format(str(datetime.now()), function_name, request_id, str(error)))
                status_code = 404 if type(error) is UnknownRecordError else 500
                return {'error_message': str(error)}, status_code
        error_handling_f.__wrapped__ = f
        return error_handling_f
    return _handle_errors_decorator

get_wine_arguments = reqparse.RequestParser()
get_wine_arguments.add_argument('id', type=int, location='args', required=True, nullable=False)

delete_wine_arguments = reqparse.RequestParser()
delete_wine_arguments.add_argument('id', type=int, location='args', required=True, nullable=False)

wines_ns = api.namespace('wines', description='API of wine datastore')

@wines_ns.route('/')
class Wines(Resource):
    @api.doc(
        description='This endpoint returns information of a wine record of a given id. The result indcludes all properties of the wine and its category.',
        id='get_wine',
        tags='Wines')
    @api.expect(get_wine_arguments, validate=True)
    @wines_circuit_breaker.decorate
    @_handle_errors('get_wine')
    def get(self):
        """
        Retrieve wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        wine = wine_facade.retrieve(id)
        classified_wine = _create_classified_wine(wine)
        return classified_wine, 200

    @api.doc(
        description='This endpoint deletes a wine record of a given id.',
        id='delete_wine',
        tags='Wines')
    @api.expect(delete_wine_arguments, validate=True)
    @wines_circuit_breaker.decorate
    @_handle_errors('delete_wine')
    def delete(self):
        """
        Delete wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        wine_facade.delete(id)
        return {}, 204

    @api.doc(
        description='This endpoint creates a wine record with a correspondening class.',
        id='create_wine',
        tags='Wines')
    @api.expect(web_model.classified_wine, validate=True)
    @wines_circuit_breaker.decorate
    @_handle_errors('create_wine')
    def post(self):
        """
        Create wine
        """
        classified_wine = request.get_json(force=True)
        id = wine_facade.create(classified_wine)
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
