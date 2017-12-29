from flask_restplus import fields

#TODO: remove nesting, create own model for each service
def create_wine(api):
    return api.model('Wine', {
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
