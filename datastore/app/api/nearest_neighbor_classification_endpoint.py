from app.api.restplus import api, web_model
from flask_restplus import Resource
from app.wine_domain.classification import initialize_nearest_neighbor_classifier
from flask import request

nearest_neighbor_ns = api.namespace('wines/classification/nearest_neighbor',
    description='API of Nearest Neighbor classification')

@nearest_neighbor_ns.route('/')
class NearestNeighbor(Resource):
    @api.doc(
        description='This endpoint returns classification of wine record using the Nearest Neighbor algorithm.',
        id='classify_nearest_neighbor',
        tags='Wines')
    @api.expect(web_model.wine, validate=True)
    #@wines_circuit_breaker.decorate
    #@_handle_errors('get_wine')
    def post(self):
        wine = request.get_json(force=True)
        classifier = initialize_nearest_neighbor_classifier()
        predicted_class = classifier.predict_class(wine)
        return {'class': predicted_class}, 200
