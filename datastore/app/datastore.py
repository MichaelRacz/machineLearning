from flask import Flask, request
from flask_restplus import Api, Resource, reqparse
import app.db_model as db_model
from app.web_model import initialize as initialize_web_model

app = Flask(__name__)
app.config.from_envvar('DATASTORE_SETTINGS')

# TODO:
# error returnen
# model initialisieren?
# weitere refactorings

api = Api(app,
    title='datastore',
    description='Manage data for machine learning services.',
    version='1.0.0',
    prefix='/v1',
    default_mediatype='application/json')

wines_ns = api.namespace('wines', description='API of wine datastore')
specification_ns = api.namespace('specification', description='Swagger specificaton of the API')

web_model = initialize_web_model(api)

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
    @api.response(200, 'Wine successfully returned.', web_model.classified_wine)
    @api.response(404, 'Unknown id.', web_model.error)
    @api.response(500, 'Unexpected server error.', web_model.error)
    def get(self):
        """
        Retrieve wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        session = db_model.Session()
        wine = session.query(db_model.Wine).filter_by(id=id).first()
        if(wine is None):
            return {'errors': {'id': "No record with id '{}' found.".format(id)}}, 404
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
        return {'wine_class': wine.wine_class, 'wine': wine_web}, 200

    @api.doc(
        description='This endpoint deletes a wine record of a given id.',
        id='delete_wine',
        tags='Wines')
    @api.expect(delete_wine_arguments, validate=True)
    @api.response(204, 'Wine successfully deleted.')
    @api.response(404, 'Unknown id.', web_model.error)
    @api.response(500, 'Unexpected server error.', web_model.error)
    def delete(self):
        """
        Delete wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        session = db_model.Session()
        wine = session.query(db_model.Wine).filter_by(id=id).first()
        if(wine is None):
            return {'errors': {'id': "No record with id '{}' found.".format(id)}}, 404
        session.delete(wine)
        session.commit()
        return {'delete': 'value'}, 204

    @api.doc(
        description='This endpoint creates a wine record with a correspondening class.',
        id='create_wine',
        tags='Wines')
    @api.expect(web_model.classified_wine, validate=True)
    @api.response(201, 'Wine successfully created.', web_model.wine_id)
    @api.response(500, 'Unexpected server error.', web_model.error)
    def post(self):
        """
        Create wine
        """
        classified_wine = request.get_json(force=True)
        merged_wine = {**{'wine_class': classified_wine['wine_class']}, **classified_wine['wine']}
        wine = db_model.Wine(**merged_wine)
        session = db_model.Session()
        session.add(wine)
        session.commit()
        return {'id': wine.id}, 201

@specification_ns.route('/swagger.json')
class Specification(Resource):
    @api.doc(
        description='This endpoint returns the swagger specification of the Wines API.',
        id='get_specification',
        tags='Specification')
    @api.response(200, 'Specification successfully returned.')
    @api.response(500, 'Unexpected server error.', web_model.error)
    def get(self):
        return json.dumps(api.__schema__)

if __name__ == '__main__':
    db_model.initialize()
    app.run(host='0.0.0.0', port=80)
