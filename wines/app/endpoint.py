from flask import Flask, request
from flask_restplus import Api
from common.app.circuit_breaker import CircuitBreaker
from flask_restplus import Resource, reqparse
from app.api.restplus import api
from wines.app import datastore
from common.app.error_handler import handle_errors
from common.app.web_model import create_wine
from flask_restplus import fields

flask_app = Flask('Wine Datastore')
flask_app.config.from_envvar('CONFIG_FILE')

api = Api(flask_app,
    title='Wine Datastore',
    description='Wine Datastore service.',
    version='1.0.0',
    prefix='/v1',
    default_mediatype='application/json')

wines_circuit_breaker = CircuitBreaker(20)
wines_ns = api.namespace('wines', description='API of wine datastore')

classified_wine = api.model('ClassifiedWine', {
    'wine': fields.Nested(create_wine(api), required=True),
    'wine_class': fields.String(required=True, enum=['1', '2', '3'])})

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
    @wines_circuit_breaker.decorate
    @handle_errors('get_wine')
    def get(self):
        """
        Retrieve wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        classified_wine = datastore.retrieve(id)
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
        datastore.delete(id)
        return {}, 204

    @api.doc(
        description='This endpoint creates a wine record with a correspondening class.',
        id='create_wine',
        tags='Wines')
    @api.expect(classified_wine, validate=True)
    @wines_circuit_breaker.decorate
    @handle_errors('create_wine')
    def post(self):
        """
        Create wine
        """
        classified_wine = request.get_json(force=True)
        id = datastore.create(classified_wine)
        return {'id': id}, 201

if __name__ == '__main__':
    try:
        database.initialize()
        wines_circuit_breaker.open()
        api.add_namespace(wines_ns)
        api.add_namespace(specification_ns)
        datastore.init(flask_app.config['KAFKA_HOSTS'], flask_app.config['WINE_TOPIC'])
        flask_app.run(host='0.0.0.0', port=80)
    finally:
        datastore.exit()