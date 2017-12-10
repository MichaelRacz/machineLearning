from common.app.circuit_breaker import CircuitBreaker
from app.api.restplus import api, web_model
from flask_restplus import Resource
from app.wine_domain.classification import classifier_factory
from flask import request
from app.api.error_handler import handle_errors

svc_circuit_breaker = CircuitBreaker(20)
svc_ns = api.namespace('wines/classification/svc', description='API of SVC classification')

@svc_ns.route('/')
class SVC(Resource):
    @api.doc(
        description='This endpoint performs classification of a wine record using the SVC algorithm.',
        id='classify_svc',
        tags='Wines')
    @api.expect(web_model.wine, validate=True)
    @svc_circuit_breaker.decorate
    @handle_errors('classify_svc')
    def post(self):
        wine = request.get_json(force=True)
        classifier = classifier_factory.create_svc_classifier()
        predicted_class = classifier.predict_class(wine)
        return {'class': predicted_class}, 200
