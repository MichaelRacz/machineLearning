import json
from nose.tools import assert_equals, assert_is_not_none, assert_dict_equal, assert_in
from app.datastore import app
import app.model as model

@given(u'I have access to the Wine API')
def step_impl(context):
    model.initialize()
    context.client = app.test_client()
    context.wines_ns = '/v1/wines/'

@given(u'I have a valid wine record')
def step_impl(context):
    wine_class = '2'
    wine_record = {
        'wine': _get_valid_wine(),
        'wine_class': wine_class}
    context.wine_record = wine_record

@given(u'All wine record properties are set to "{value:d}"')
def step_impl(context, value):
    wine = context.wine_record['wine']
    for key in wine.keys():
        wine[key] = value

@given(u'I have a wine record without a wine class')
def step_impl(context):
    context.wine_record = {'wine': _get_valid_wine()}

@given(u'I have a wine record without a wine')
def step_impl(context):
    context.wine_record = {'wine_class': '1'}

@given(u'I have a wine record with a wine without property "{property}"')
def step_impl(context, property):
    wine = _get_valid_wine()
    del wine[property]
    wine_record = {
        'wine': wine,
        'wine_class': '3'}
    context.wine_record = wine_record

@given(u'I have a wine record with a wine class "{wine_class}"')
def step_impl(context, wine_class):
    wine_record = {
        'wine': _get_valid_wine(),
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

@then(u'I receive a validation error indicating a missing required property')
def step_impl(context):
    error_messages = list(context.response_content['errors'].values())
    assert_equals(len(error_messages), 1)
    assert_in('is a required property', error_messages[0])

@then(u'I receive a validation error indicating an invalid value for wine class')
def step_impl(context):
    error_message = context.response_content['errors']['wine_class']
    assert_in("is not one of ['1', '2', '3']", error_message)

@then(u'I receive a validation error for all properties indicating an invalid value')
def step_impl(context):
    for key in context.wine_record['wine'].keys():
        property_identifier = 'wine.{}'.format(key)
        assert_in('-1 is less than the minimum of 0', context.response_content['errors'][property_identifier])

@then(u'I GET the record from the get_wine endpoint')
def step_impl(context):
    response = context.client \
        .get('{}?id={}'.format(context.wines_ns, context.response_content['id']))
    _add_response_to_context(context, response)
    assert_dict_equal(context.response_content, context.wine_record)

@then(u'the HTTP status code is "{expected_status_code:d}"')
def step_impl(context, expected_status_code):
    assert_equals(context.response.status_code ,expected_status_code)

def _add_response_to_context(context, response):
    context.response = response
    context.response_content = json.loads(response.get_data(as_text=True))

def _get_valid_wine():
    return {
        'alcohol': 0.0,
        'malic_acid': 1.1,
        'ash': 2.2,
        'alcalinity_of_ash': 3.3,
        'magnesium':  5,
        'total_phenols': 6.6,
        'flavanoids': 7.7,
        'nonflavanoid_phenols': 8.8,
        'proanthocyanins': 9.9,
        'color_intensity': 10.1,
        'hue': 11.1,
        'odxxx_of_diluted_wines': 12.1,
        'proline': 13}
