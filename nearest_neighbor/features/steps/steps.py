from classification_contract.wine_test_data.utilities import split_wine_data
from classification_contract.messages import create_create_message
from nearest_neighbor.app import endpoint
import json
from nose.tools import assert_equals, assert_greater

@given(u'the nearest neighbor service is initialized with a training set')
def step_impl(context):
    training_set, context.test_set = split_wine_data()
    produce_messages(context, training_set)
    endpoint.init()
    context.client = endpoint.flask_app.test_client()

def produce_messages(context, training_set):
    producer = context.test_log_backend.create_producer()
    i = 0
    while i < len(training_set):
        message = create_create_message(i, training_set[i])
        producer.produce(json.dumps(message).encode('utf-8'))
        i += 1

@when(u'I classify the test set using the Nearest Neighbor algorithm')
def step_impl(context):
    classification_results = []
    for classified_wine in context.test_set:
        wine = classified_wine['wine']
        response = context.client.post('/v1/nearest_neighbor/',
            data=json.dumps(wine),
            headers={'content-type':'application/json'})
        assert_equals(response.status_code, 200)
        response_content = json.loads(response.get_data(as_text=True))
        classification_results.append(response_content['class'])
    context.classification_results = classification_results

@then(u'the test set is classified correctly, regarding suitable tolerance')
def step_impl(context):
    correct_classifications = 0
    for i in range(0, len(context.test_set)):
        expected_class = context.test_set[i]['wine_class']
        actual_class = context.classification_results[i]
        if(actual_class == expected_class):
            correct_classifications += 1
    success = correct_classifications / len(context.test_set)
    # NOTE: actual success rate is almost 100 %
    assert_greater(success, 0.9)
