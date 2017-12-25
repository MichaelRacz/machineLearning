from flask import Flask, request
from flask_restplus import Api
from common.app.circuit_breaker import CircuitBreaker
from flask_restplus import Resource
from common.app.error_handler import handle_errors
from common.app.web_model import create_wine
from svc.app import classification

flask_app = Flask('SVC')
flask_app.config.from_envvar('CONFIG_FILE')

api = Api(flask_app,
    title='SVC classification',
    description='SVC classification service.',
    version='1.0.0',
    prefix='/v1',
    default_mediatype='application/json')

svc_circuit_breaker = CircuitBreaker(20)
svc_ns = api.namespace('wines/classification/svc', description='API for SVC classification')
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
        predicted_class = classification.predict_class(wine)
        return {'class': predicted_class}, 200

if __name__ == '__main__':
    svc.init()
    svc_circuit_breaker.open()
    api.add_namespace(svc_ns)
    #TODO: fix specification
    #api.add_namespace(specification_ns)
    flask_app.run(host='0.0.0.0', port=80)
