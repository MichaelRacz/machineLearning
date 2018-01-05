from flask import Flask, request
from flask_restplus import Api
from common.app.circuit_breaker import CircuitBreaker
from flask_restplus import Resource, reqparse
from wines.app import datastore, database
from common.app.error_handler import handle_errors
from flask_restplus import fields
from contextlib import ContextDecorator

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

wine = api.model('Wine', {
    'alcohol': fields.Float(required=True, min=0.0),
    'malic_acid': fields.Float(required=True, min=0.0),
    'ash': fields.Float(required=True, min=0.0),
    'alcalinity_of_ash': fields.Float(required=True, min=0.0),
    'magnesium':  fields.Integer(required=True, min=0),
    'total_phenols': fields.Float(required=True, min=0.0),
    'flavanoids': fields.Float(required=True, min=0.0),
    'nonflavanoid_phenols': fields.Float(required=True, min=0.0),
    'proanthocyanins': fields.Float(required=True, min=0.0),
    'color_intensity': fields.Float(required=True, min=0.0),
    'hue': fields.Float(required=True, min=0.0),
    'odxxx_of_diluted_wines': fields.Float(required=True, min=0.0, description='description: OD280/OD315 of diluted wines'),
    'proline': fields.Integer(required=True, min=0)})

classified_wine = api.model('ClassifiedWine', {
    'wine': fields.Nested(wine, required=True),
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

@wines_ns.route('/swagger.json')
class Specification(Resource):
    def get(self):
        return json.dumps(api.__schema__), 200

class InitializationScope(ContextDecorator):
    def __enter__(self):
        database.initialize()
        wines_circuit_breaker.open()
        api.add_namespace(wines_ns)
        datastore.init(flask_app.config['KAFKA_HOSTS'], flask_app.config['WINE_TOPIC'])
        return self

    def __exit__(self, *exc):
        datastore.exit()
        return False

if __name__ == '__main__':
    with InitializationScope():
        flask_app.run(host='0.0.0.0', port=port)
