from flask import Flask, request
from flask_restplus import Api
from common.app.circuit_breaker import CircuitBreaker
from flask_restplus import Resource
from common.app.error_handler import handle_errors
from common.app.web_model import create_wine
from nearest_neighbor.app import classification

flask_app = Flask('Nearest Neighbor')
flask_app.config.from_envvar('CONFIG_FILE')

api = Api(flask_app,
    title='Nearest Neighbor classification',
    description='Nearest Neighbor classification service.',
    version='1.0.0',
    prefix='/v1',
    default_mediatype='application/json')

nearest_neighbor_circuit_breaker = CircuitBreaker(20)

nearest_neighbor_ns = api.namespace('nearest_neighbor',
    description='API for Nearest Neighbor classification')

wine = create_wine(api)

@nearest_neighbor_ns.route('/')
class NearestNeighbor(Resource):
    @api.doc(
        description='This endpoint returns classification of wine record using the Nearest Neighbor algorithm.',
        id='classify_nearest_neighbor',
        tags='Wines')
    @api.expect(wine, validate=True)
    @nearest_neighbor_circuit_breaker.decorate
    @handle_errors('classify_nearest_neighbor')
    def post(self):
        wine = request.get_json(force=True)
        predicted_class = classification.predict_class(wine)
        return {'class': predicted_class}, 200

@nearest_neighbor_ns.route('/swagger.json')
class Specification(Resource):
    def get(self):
        return json.dumps(api.__schema__), 200

def init():
    classification.init(flask_app.config['KAFKA_HOSTS'], flask_app.config['WINE_TOPIC'])
    nearest_neighbor_circuit_breaker.open()
    api.add_namespace(nearest_neighbor_ns)

if __name__ == '__main__':
    init()
    flask_app.run(host='0.0.0.0', port=80)
