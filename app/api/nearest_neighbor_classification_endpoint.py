from common.app.circuit_breaker import CircuitBreaker
from app.api.restplus import api
from flask_restplus import Resource
from app.wine_domain.classification import classifier_factory
from flask import request
from common.app.error_handler import handle_errors
from common.app.web_model import create_wine

nearest_neighbor_ns = api.namespace('wines/classification/nearest_neighbor',
    description='API for Nearest Neighbor classification')

nearest_neighbor_circuit_breaker = CircuitBreaker(20)
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
        classifier = classifier_factory.create_nearest_neighbor_classifier()
        predicted_class = classifier.predict_class(wine)
        return {'class': predicted_class}, 200
