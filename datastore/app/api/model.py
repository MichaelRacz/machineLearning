from flask_restplus import fields

def initialize(api):
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
        'error_message': fields.String(required=True)})

    return WebModel(wine, classified_wine, wine_id, error)

class WebModel:
    def __init__(self, wine, classified_wine, wine_id, error):
        self.wine = wine
        self.classified_wine = classified_wine
        self.wine_id = wine_id
        self.error = error
