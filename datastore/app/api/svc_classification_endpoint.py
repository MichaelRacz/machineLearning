from app.api.restplus import api, web_model
from flask_restplus import Resource
from app.wine_domain.classification import initialize_svc_classifier
from flask import request

svc_ns = api.namespace('wines/classification/svc', description='API of SVC classification')
classifier = None

@svc_ns.route('/')
class SVC(Resource):
    @api.doc(
        description='This endpoint returns classification of wine record using the SVC algorithm.',
        id='classify_svc',
        tags='Wines')
    @api.expect(web_model.wine, validate=True)
    #@wines_circuit_breaker.decorate
    #@_handle_errors('get_wine')
    def post(self):
        wine = request.get_json(force=True)
        if classifier is None:
            classifier = initialize_svc_classifier()
        predicted_class = classifier.predict(wine)[0]
        return {'class': predicted_class}, 200
