from app.api.restplus import api, web_model
from flask_restplus import Resource
from app.wine_domain.classification import initialize_nearest_neighbor_classifier
from flask import request
from app.api.error_handler import handle_errors
from app.api.circuit_breaker import CircuitBreaker

nearest_neighbor_ns = api.namespace('wines/classification/nearest_neighbor',
    description='API of Nearest Neighbor classification')

nearest_neighbor_circuit_breaker = CircuitBreaker(20)

@nearest_neighbor_ns.route('/')
class NearestNeighbor(Resource):
    @api.doc(
        description='This endpoint returns classification of wine record using the Nearest Neighbor algorithm.',
        id='classify_nearest_neighbor',
        tags='Wines')
    @api.expect(web_model.wine, validate=True)
    @nearest_neighbor_circuit_breaker.decorate
    @handle_errors('classify_nearest_neighbor')
    def post(self):
        wine = request.get_json(force=True)
        classifier = initialize_nearest_neighbor_classifier()
        predicted_class = classifier.predict_class(wine)
        return {'class': predicted_class}, 200
