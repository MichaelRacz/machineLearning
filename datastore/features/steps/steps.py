import json
from nose.tools import assert_equals, assert_is_not_none, assert_dict_equal
from app.datastore import app
import app.model as model

@given(u'I have access to the Wine API')
def step_impl(context):
    model.initialize()
    context.client = app.test_client()
    context.wines_ns = '/v1/wines/'

@given(u'I have a valid wine record')
def step_impl(context):
    wine = {
        'alcohol': 0.0,
        'malic_acid': 1.0,
        'ash': 2.0,
        'alcalinity_of_ash': 3.0,
        'magnesium':  5,
        'total_phenols': 6.0,
        'flavanoids': 7.0,
        'nonflavanoid_phenols': 8.0,
        'proanthocyanins': 9.0,
        'color_intensity': 10.0,
        'hue': 11.0,
        'odxxx_of_diluted_wines': 12.0,
        'proline': 13}
    wine_class = '2'
    wine_record = {
        'wine': wine,
        'wine_class': wine_class}
    context.wine_record = wine_record

@when(u'I POST it to the create_wine endpoint')
def step_impl(context):
    response = context.client.post(context.wines_ns,
        data=json.dumps(context.wine_record),
        headers={'content-type':'application/json'})
    _add_response_to_context(context, response)

@then(u'I receive the id of created wine record')
def step_impl(context):
    assert_is_not_none(context.response_content['id'])

@then(u'I GET the record from the get_wine endpoint')
def step_impl(context):
    response = context.client \
        .get('{}?id={}'.format(context.wines_ns, context.response_content['id']))
    _add_response_to_context(context, response)
    assert_dict_equal(context.response_content, context.wine_record)

def _add_response_to_context(context, response):
    context.response = response
    context.response_content = json.loads(response.get_data(as_text=True))
