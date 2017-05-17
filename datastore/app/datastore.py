from flask import Flask, request
from flask_restplus import Api, Resource, reqparse, fields
import app.model as model

app = Flask(__name__)

api = Api(app,
    title='datastore',
    description='Manage data for machine learning services.',
    version='1.0.0',
    prefix='/v1',
    default_mediatype='application/json')

wines_ns = api.namespace('wines', description='API of wine datastore')
specification_ns = api.namespace('specification', description='Swagger specificaton of the API')

wine = api.model('Wine', {
    'alcohol': fields.Float(required=True, min=0.0),
    'malic_acid': fields.Float(required=True, min=0.0),
    'ash': fields.Float(required=True, min=0.0),
    'alcalinity_of_ash': fields.Float(required=True, min=0.0),
    'magnesium':  fields.Integer(required=True, min=0),
    'total_phenols': fields.Float(required=True, min=0.0),
    'flavanoids': fields.Float(required=True, min=0.0),
    'nonflavanoid_phenols': fields.Float(required=True, min=0.0),
    'proanthocyanins': fields.Float(required=True, min=0.0),
    'color_intensity': fields.Float(required=True, min=0.0),
    'hue': fields.Float(required=True, min=0.0),
    'odxxx_of_diluted_wines': fields.Float(required=True, min=0.0, description='description: OD280/OD315 of diluted wines'),
    'proline': fields.Integer(required=True, min=0)})

classified_wine = api.model('ClassifiedWine', {
    'wine': fields.Nested(wine, required=True),
    'wine_class': fields.String(required=True, enum=['1', '2', '3'])})

wine_id = api.model('WineId', {
    'id': fields.String(required=True)})

error = api.model('Error', {
    'code': fields.Integer(required=True),
    'message': fields.String(required=True)})

get_wine_arguments = reqparse.RequestParser()
get_wine_arguments.add_argument('id', type=int, location='args', required=True, nullable=False)

delete_wine_arguments = reqparse.RequestParser()
delete_wine_arguments.add_argument('id', type=int, location='args', required=True, nullable=False)

@wines_ns.route('/')
class Wines(Resource):
    @api.doc(
        description='This endpoint returns information of a wine record of a given id. The result indcludes all properties of the wine and its category.',
        id='get_wine',
        tags='Wines')
    @api.expect(get_wine_arguments, validate=True)
    @api.response(200, 'Wine successfully returned.', classified_wine)
    @api.response(404, 'Unknown id.', error)
    @api.response(422, 'Malformed id.', error)
    @api.response(500, 'Unexpected server error.', error)
    def get(self):
        """
        Retrieve wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        session = model.Session()
        wine = session.query(model.Wine).filter_by(id=id).first()
        session.rollback()
        wine_web = { \
            'alcohol': wine.alcohol, \
            'malic_acid': wine.malic_acid,
            'ash': wine.ash,
            'alcalinity_of_ash': wine.alcalinity_of_ash,
            'magnesium': wine.magnesium,
            'total_phenols': wine.total_phenols,
            'flavanoids': wine.flavanoids,
            'nonflavanoid_phenols': wine.nonflavanoid_phenols,
            'proanthocyanins': wine.proanthocyanins,
            'color_intensity': wine.color_intensity,
            'hue': wine.hue,
            'odxxx_of_diluted_wines': wine.odxxx_of_diluted_wines,
            'proline': wine.proline}
        return {'wine_class': wine.wine_class, 'wine': wine_web}

    @api.doc(
        description='This endpoint deletes a wine record of a given id.',
        id='delete_wine',
        tags='Wines')
    @api.expect(delete_wine_arguments, validate=True)
    @api.response(204, 'Wine successfully deleted.')
    @api.response(404, 'Unknown id.', error)
    @api.response(422, 'Malformed id.', error)
    @api.response(500, 'Unexpected server error.', error)
    def delete(self):
        """
        Delete wine
        """
        return {'delete': 'value'}

    @api.doc(
        description='This endpoint creates a wine record with a correspondening class.',
        id='create_wine',
        tags='Wines')
    @api.expect(classified_wine, validate=True)
    @api.response(201, 'Wine successfully created.', wine_id)
    @api.response(422, 'Malformed id.', error)
    @api.response(500, 'Unexpected server error.', error)
    def post(self):
        """
        Create wine
        """
        classified_wine = request.get_json(force=True)
        merged_wine = {**{'wine_class': classified_wine['wine_class']}, **classified_wine['wine']}
        wine = model.Wine(**merged_wine)
        session = model.Session()
        session.add(wine)
        session.commit()
        return {'id': wine.id}

@specification_ns.route('/swagger.json')
class Specification(Resource):
    @api.doc(
        description='This endpoint returns the swagger specification of the Wines API.',
        id='get_specification',
        tags='Specification')
    @api.response(200, 'Specification successfully returned.')
    @api.response(500, 'Unexpected server error.', error)
    def get(self):
        return json.dumps(api.__schema__)

if __name__ == '__main__':
    model.initialize()
    app.run(debug=True)
