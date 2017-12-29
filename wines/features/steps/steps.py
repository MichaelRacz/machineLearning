import json
from nose.tools import assert_equals, assert_is_not_none, assert_dict_equal, assert_in, assert_true
import sys
from behave import given, when, then

@given(u'I have a valid wine record')
def step_impl(context):
    wine_class = '2'
    context.wine_record = _create_classified_wine(_create_wine(), wine_class)

@given(u'All wine record properties are set to "{value:d}"')
def step_impl(context, value):
    wine = context.wine_record['wine']
    for key in wine.keys():
        wine[key] = value

@given(u'I have a wine record without a wine class')
def step_impl(context):
    context.wine_record = {'wine': _create_wine()}

@given(u'I have a wine record without a wine')
def step_impl(context):
    context.wine_record = {'wine_class': '1'}

@given(u'I have a wine record with a wine without property "{property}"')
def step_impl(context, property):
    wine = _create_wine()
    del wine[property]
    context.wine_record = _create_classified_wine(wine, '3')

@given(u'I have a wine record with a wine class "{wine_class}"')
def step_impl(context, wine_class):
    context.wine_record = _create_classified_wine(_create_wine(), wine_class)

@given(u'I POST it to the create_wine endpoint')
@when(u'I POST it to the create_wine endpoint')
def step_impl(context):
    response = _post_wine_record(context, context.wine_record)
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

@then(u'I receive an error indicating that there is no record with the given id')
def step_impl(context):
    error_message = context.response_content['error_message']
    assert_in("No record with id '{}' found.".format(context.id), error_message)

@then(u'I receive an error indicating that the id is malformed')
def step_impl(context):
    error_message = context.response_content['errors']['id']
    assert_in("invalid literal for int() with base 10: '{}'".format(context.id), error_message)

@then(u'I GET the record from the get_wine endpoint')
def step_impl(context):
    _get_wine(context, context.response_content['id'])
    assert_dict_equal(context.response_content, context.wine_record)

@when(u'I GET the record from the get_wine endpoint')
def step_impl(context):
    context.id = context.response_content['id']
    _get_wine(context, context.id)

@when(u'I GET a record with the id "{id}"')
def step_impl(context, id):
    context.id = id
    _get_wine(context, id)

@when(u'I DELETE the record')
def step_impl(context):
    _delete_wine(context, context.response_content['id'])

@when(u'I DELETE a record with the id "{id}"')
def step_impl(context, id):
    context.id = id
    _delete_wine(context, id)

@then(u'the HTTP status code is "{expected_status_code:d}"')
def step_impl(context, expected_status_code):
    assert_equals(context.response.status_code, expected_status_code)

@when(u'I log some create and delete entries')
def step_impl(context):
    producer = context.test_log_backend.create_producer()
    classified_wines = [
        _create_classified_wine(_create_wine(), '1'),
        _create_classified_wine(_create_wine(), '2')]
    events = [
        _create_create_event(1, classified_wines[0]),
        _create_create_event(2, classified_wines[1]),
        _create_delete_event(2),
        _create_create_event(3, classified_wines[0]),
        _create_create_event(4, classified_wines[1]),
        _create_delete_event(3)]
    _produce_events(events, producer)
    context.stored_wines = [
        {'id': 1, 'classified_wine': classified_wines[0]},
        {'id': 4, 'classified_wine': classified_wines[1]}]
    context.deleted_wine_ids = [2, 3]

def _create_create_event(id, classified_wine):
    return {
        'type': 'create',
        'version': '1',
        'id': id,
        'classified_wine': classified_wine
    }

def _create_delete_event(id):
    return {
        'type': 'delete',
        'version': '1',
        'id': id
    }

def _produce_events(events, producer):
    for event in events:
        producer.produce(json.dumps(event).encode('utf-8'))

@then(u'the create entries can be received')
def step_impl(context):
    for stored_wine in context.stored_wines:
        _get_wine(context, stored_wine['id'])
        assert_dict_equal(context.response_content, stored_wine['classified_wine'])

@then(u'the delete entries cannot be received')
def step_impl(context):
    for id in context.deleted_wine_ids:
        _get_wine(context, id)
        assert_equals(context.response.status_code, 404)

def _create_classified_wine(wine, wine_class):
    return {
        'wine': wine,
        'wine_class': wine_class}

def _create_wine(alcohol = 0.0,
    malic_acid = 1.1,
    ash = 2.2,
    alcalinity_of_ash = 3.3,
    magnesium =  5,
    total_phenols = 6.6,
    flavanoids = 7.7,
    nonflavanoid_phenols = 8.8,
    proanthocyanins = 9.9,
    color_intensity = 10.1,
    hue = 11.1,
    odxxx_of_diluted_wines = 12.1,
    proline = 13):
    return {
        'alcohol': alcohol,
        'malic_acid': malic_acid,
        'ash': ash,
        'alcalinity_of_ash': alcalinity_of_ash,
        'magnesium':  magnesium,
        'total_phenols': total_phenols,
        'flavanoids': flavanoids,
        'nonflavanoid_phenols': nonflavanoid_phenols,
        'proanthocyanins': proanthocyanins,
        'color_intensity': color_intensity,
        'hue': hue,
        'odxxx_of_diluted_wines': odxxx_of_diluted_wines,
        'proline': proline}

def _post_wine_record(context, classified_wine):
    return context.client.post(context.wines_ns,
        data=json.dumps(classified_wine),
        headers={'content-type':'application/json'})

def _get_wine(context, id):
    response = context.client \
        .get('{}?id={}'.format(context.wines_ns, id))
    _add_response_to_context(context, response)

def _delete_wine(context, id):
    response = context.client \
        .delete('{}?id={}'.format(context.wines_ns, id))
    _add_response_to_context(context, response)

def _add_response_to_context(context, response):
    context.response = response
    response_data = response.get_data(as_text=True)
    if(response_data != ''):
        context.response_content = json.loads(response_data)
