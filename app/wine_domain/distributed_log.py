from pykafka import KafkaClient
from app.api.restplus import flask_app
import json
from pykafka.common import OffsetType

def read():
    client = KafkaClient(hosts=flask_app.config['KAFKA_HOSTS'])
    topic = client.topics[flask_app.config['WINE_TOPIC'].encode('ascii')]
    consumer = topic.get_simple_consumer(
        auto_offset_reset=OffsetType.EARLIEST,
        reset_offset_on_start=True,
        consumer_timeout_ms=500) #TODO create config var or refactor
    wines = {}
    for encoded_message in consumer:
        if encoded_message is not None:
            message = json.loads(encoded_message.value.decode('utf-8'))
            _handle_message(message, wines)
    return wines

def _handle_message(message, wines):
    if message['type'] == 'create':
        wines[message['id']] = message['classified_wine']
    if message['type'] == 'delete':
        wine.pop(message['id'])
