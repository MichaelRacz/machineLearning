from flask import request
from flask_restplus import Resource, reqparse
from app.api.restplus import api, web_model
import app.wine_domain.facade as wine_facade
from app.api.error_handler import handle_errors
from app.api.circuit_breaker import CircuitBreaker

get_wine_arguments = reqparse.RequestParser()
get_wine_arguments.add_argument('id', type=int, location='args', required=True, nullable=False)

delete_wine_arguments = reqparse.RequestParser()
delete_wine_arguments.add_argument('id', type=int, location='args', required=True, nullable=False)

wines_ns = api.namespace('wines', description='API of wine datastore')
# TODO make configurable
wines_circuit_breaker = CircuitBreaker(20)

@wines_ns.route('/')
class Wines(Resource):
    @api.doc(
        description='This endpoint returns information of a wine record of a given id. The result indcludes all properties of the wine and its category.',
        id='get_wine',
        tags='Wines')
    @api.expect(get_wine_arguments, validate=True)
    @wines_circuit_breaker.decorate
    @handle_errors('get_wine')
    def get(self):
        """
        Retrieve wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        classified_wine = wine_facade.retrieve(id)
        return classified_wine, 200

    @api.doc(
        description='This endpoint deletes a wine record of a given id.',
        id='delete_wine',
        tags='Wines')
    @api.expect(delete_wine_arguments, validate=True)
    @wines_circuit_breaker.decorate
    @handle_errors('delete_wine')
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
    @handle_errors('create_wine')
    def post(self):
        """
        Create wine
        """
        classified_wine = request.get_json(force=True)
        id = wine_facade.create(classified_wine)
        return {'id': id}, 201
