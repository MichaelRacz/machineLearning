from classification_contract.wine_test_data.utilities import get_classified_wine
from classification_contract.assertions import assert_create_message_structure, assert_delete_message_structure
from pykafka import KafkaClient
from pykafka.common import OffsetType
import json

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

consumer_timeout_ms = 100

def load_classified_wines(hosts, topic):
    wines = {}
    for message in read_all_messages(hosts, topic):
        if message['type'] == 'create':
            wines[message['id']] = message['classified_wine']
        if message['type'] == 'delete':
            wine.pop(message['id'])
    return wines.values()

def read_all_messages(hosts, topic):
    client = KafkaClient(hosts=hosts)
    topic = client.topics[topic.encode('ascii')]
    consumer = topic.get_simple_consumer(
        auto_offset_reset=OffsetType.EARLIEST,
        reset_offset_on_start=True,
        consumer_timeout_ms=consumer_timeout_ms)
    for encoded_message in consumer:
        if encoded_message is not None:
            yield json.loads(encoded_message.value.decode('utf-8'))
