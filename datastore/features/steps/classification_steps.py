from features.steps.step_utilities import post_wine_record, create_wine, create_classified_wine
from features.steps.wine_data import wine_data
from random import random
from nose.tools import assert_equals, assert_greater
import json

@given(u'the datastore contains a training set')
def step_impl(context):
    training_set = []
    context.test_set = []
    for record in wine_data:
        if random() < 0.7:
            training_set.append(record)
        else:
            context.test_set.append(record)
    for record in training_set:
        wine = _extract_wine(record)
        wine_class = str(record[0])
        classified_wine = create_classified_wine(wine, wine_class)
        response = post_wine_record(context, classified_wine)
        assert_equals(response.status_code, 201)

@when(u'I classify the test set using the SVC algorithm')
def step_impl(context):
    classification_results = []
    for record in context.test_set:
        wine = _extract_wine(record)
        response = context.client.post(context.svc_ns,
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
        expected_class = str(context.test_set[i][0])
        actual_class = context.classification_results[i]
        if(actual_class == expected_class):
            correct_classifications += 1
    success = correct_classifications / len(context.test_set)
    # NOTE: actual success rate is almost 100 %
    assert_greater(success, 0.9)


def _extract_wine(record):
    record_without_class = record[1:]
    return create_wine(*record_without_class)
