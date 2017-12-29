from nose.tools import assert_is_instance, assert_greater, assert_equals, assert_is_not_none, assert_in

wine_properties = {
    'alcohol': float,
    'malic_acid': float,
    'ash': float,
    'alcalinity_of_ash': float,
    'magnesium':  int,
    'total_phenols': float,
    'flavanoids': float,
    'nonflavanoid_phenols': float,
    'proanthocyanins': float,
    'color_intensity': float,
    'hue': float,
    'odxxx_of_diluted_wines': float,
    'proline': int}

def assert_classified_wine_structure(classified_wine):
    assert_in(classified_wine['wine_class'], [str(i) for i in range(1, 4)])
    wine = classified_wine['wine']
    for property in wine_properties.keys():
        value = wine[property]
        assert_is_instance(value, wine_properties[property])
        assert_greater(value, 0)

def assert_create_message_structure(message):
    _assert_common_properties(message, 'create')
    assert_classified_wine_structure(message['classified_wine'])

def assert_delete_message_structure(message):
    _assert_common_properties(message, 'delete')

def _assert_common_properties(message, message_type):
    assert_equals(message['type'], message_type)
    assert_equals(message['version'], '1')
    assert_is_not_none(message['id'])
