from app.api.restplus import api, web_model
from flask_restplus import Resource

svc_ns = api.namespace('wines/classification/svc', description='API of SVC classification')

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
        return {'class': '2'}, 200
