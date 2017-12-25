from common.app.circuit_breaker import CircuitBreaker
from app.api.restplus import api
from flask_restplus import Resource
from flask import request
from common.app.error_handler import handle_errors
from common.app.web_model import create_wine
from app.wine_domain import svc

svc_ns = api.namespace('wines/classification/svc', description='API of SVC classification')
svc_circuit_breaker = CircuitBreaker(20)
wine = create_wine(api)

@svc_ns.route('/')
class SVC(Resource):
    @api.doc(
        description='This endpoint performs classification of a wine record using the SVC algorithm.',
        id='classify_svc',
        tags='Wines')
    @api.expect(wine, validate=True)
    @svc_circuit_breaker.decorate
    @handle_errors('classify_svc')
    def post(self):
        wine = request.get_json(force=True)
        predicted_class = svc.predict_class(wine)
        return {'class': predicted_class}, 200
