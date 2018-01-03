from classification_contract.wine_test_data.utilities import get_classified_wine
import json
from classification_contract.messages import create_create_message, create_delete_message, read_all_messages
from nose.tools import assert_equals, assert_dict_equal

@given(u'I have a classified wine')
def step_impl(context):
    context.classified_wine = get_classified_wine()

@given(u'I POST it to the wines endpoint')
@when(u'I POST it to the wines endpoint')
def step_impl(context):
    response = context.client.post('v1/wines/',
        data=json.dumps(context.classified_wine),
        headers={'content-type':'application/json'})
    assert_equals(response.status_code, 201)
    response_content = json.loads(response.get_data(as_text=True))
    context.classified_wine_id = response_content['id']

@when(u'I DELETE the record')
def step_impl(context):
    response = context.client.delete('v1/wines/?id={}'.format(context.classified_wine_id))
    assert_equals(response.status_code, 204)

@then(u'the creation is logged')
def step_impl(context):
    expected_message = create_create_message(context.classified_wine_id, context.classified_wine)
    _assert_contains_message(context, expected_message)

@then(u'the deletion is logged')
def step_impl(context):
    expected_message = create_create_message(context.classified_wine_id)
    _assert_contains_message(context, expected_message)

def _assert_contains_message(context, expected_message):
    messages = read_all_messages(context.test_log_backend.hosts, context.test_log_backend.topic_name)
    matching_messages = [message for message in messages
        if message['type'] == expected_message['type']
        and message['id'] == expected_message['id']]
    assert_equals(1, len(matching_messages), 'no/too many matching messages logged')
    assert_dict_equal(matching_messages[0], expected_message)
