from classification_contract.wine_test_data.utilities import get_classified_wine
from classification_contract.assertions import assert_create_message_structure, assert_delete_message_structure

def create_create_message(id=1, classified_wine=None):
    message = {
        'type': 'create',
        'version': '1',
        'id': id,
        'classified_wine': classified_wine if classified_wine is not None else get_classified_wine()
    }
    assert_create_message_structure(message)
    return message

def create_delete_message(id=1):
    message = {
        'type': 'delete',
        'version': '1',
        'id': id
    }
    assert_delete_message_structure(message)
    return message
