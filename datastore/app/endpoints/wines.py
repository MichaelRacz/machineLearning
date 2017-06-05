from flask import request
from flask_restplus import Resource, reqparse
from app.endpoints.api import api
from app.web_model import initialize as initialize_web_model
import app.wine_crud as wine_crud
from app.wine_crud import UnknownRecordError

wines_ns = api.namespace('wines', description='API of wine datastore')
web_model = initialize_web_model(api)

get_wine_arguments = reqparse.RequestParser()
get_wine_arguments.add_argument('id', type=int, location='args', required=True, nullable=False)

delete_wine_arguments = reqparse.RequestParser()
delete_wine_arguments.add_argument('id', type=int, location='args', required=True, nullable=False)

def handle_errors(f):
    def error_handling_f(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except UnknownRecordError as error:
            return {'error_message': error.message}, 404
    return error_handling_f

def _create_classified_wine(wine):
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
    @handle_errors
    def get(self):
        """
        Retrieve wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        wine = wine_crud.retrieve(id)
        classified_wine = _create_classified_wine(wine)
        return classified_wine, 200

    @api.doc(
        description='This endpoint deletes a wine record of a given id.',
        id='delete_wine',
        tags='Wines')
    @api.expect(delete_wine_arguments, validate=True)
    @api.response(204, 'Wine successfully deleted.')
    @api.response(404, 'Unknown id.', web_model.error)
    @api.response(500, 'Unexpected server error.', web_model.error)
    @handle_errors
    def delete(self):
        """
        Delete wine
        """
        args = get_wine_arguments.parse_args()
        id = args['id']
        wine_crud.delete(id)
        return {}, 204

    @api.doc(
        description='This endpoint creates a wine record with a correspondening class.',
        id='create_wine',
        tags='Wines')
    @api.expect(web_model.classified_wine, validate=True)
    @api.response(201, 'Wine successfully created.', web_model.wine_id)
    @api.response(500, 'Unexpected server error.', web_model.error)
    @handle_errors
    def post(self):
        """
        Create wine
        """
        classified_wine = request.get_json(force=True)
        id = wine_crud.create(classified_wine)
        return {'id': id}, 201
