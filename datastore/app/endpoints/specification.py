from flask_restplus import Resource
from app.endpoints.api import api

specification_ns = api.namespace('specification', description='Swagger specificaton of the API')

@specification_ns.route('/swagger.json')
class Specification(Resource):
    @api.doc(
        description='This endpoint returns the swagger specification of the Wines API.',
        id='get_specification',
        tags='Specification')
    @api.response(200, 'Specification successfully returned.')
    def get(self):
        return json.dumps(api.__schema__), 200
