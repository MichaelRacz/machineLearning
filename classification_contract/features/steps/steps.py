import json
from nose.tools import assert_equals, assert_dict_equal
from wines.features.steps.steps import *

@then(u'the creation is logged')
def step_impl(context):
    expected_event = {
        'type': 'create',
        'version': '1',
        'id': context.response_content['id'],
        'classified_wine': context.wine_record
    }
    _assert_contains_message(context, expected_event)

@then(u'the deletion is logged')
def step_impl(context):
    expected_event = {
        'type': 'delete',
        'version': '1',
        'id': context.response_content['id']
    }
    _assert_contains_message(context, expected_event)

def _assert_contains_message(context, expected_message):
    consumer = context.test_log_backend.create_consumer()
    messages = [json.loads(message.value.decode('utf-8')) for message in consumer if message is not None]
    matching_messages = [message for message in messages
        if message['type'] == expected_message['type']
        and message['id'] == expected_message['id']]
    assert_equals(1, len(matching_messages))
    assert_dict_equal(matching_messages[0], expected_message)
