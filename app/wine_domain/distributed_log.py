from pykafka import KafkaClient
from app.api.restplus import flask_app
import json
from pykafka.common import OffsetType
from pykafka.exceptions import ConsumerStoppedException

class DistributedLog:
    def __enter__(self):
        self._client = KafkaClient(hosts=flask_app.config['KAFKA_HOSTS'])
        self._topic = self._client.topics[flask_app.config['WINE_TOPIC'].encode('ascii')]
        self._producer = self._topic.get_sync_producer()
        self._consumer = self._topic.get_simple_consumer(
            auto_offset_reset=OffsetType.EARLIEST,
            reset_offset_on_start=False)
        self._read_stopped = False
        return self

    def __exit__(self, type, value, traceback):
        self._producer.__exit__(None, None, None)
        self.stop_read()

    def read(self):
        try:
            for message in self._consumer:
                if message is not None:
                    yield json.loads(message.value.decode('utf-8'))
        except ConsumerStoppedException as exception:
            if self._read_stopped == False:
                raise exception

    def stop_read(self):
        self._read_stopped = True
        self._consumer.stop()

    def log_create(self, id, classified_wine):
        event = {
            'type': 'create',
            'version': '1',
            'id': id,
            'classified_wine': classified_wine
        }
        self._producer.produce(json.dumps(event).encode('utf-8'))

    def log_delete(self, id):
        event = {
            'type': 'delete',
            'version': '1',
            'id': id
        }
        self._producer.produce(json.dumps(event).encode('utf-8'))

class DistributedLogContext:
    _log = None

    def get_log():
        if DistributedLogContext._log == None:
            log = DistributedLog()
            log.__enter__()
            DistributedLogContext._log = log
        return DistributedLogContext._log

    def free_log():
        if DistributedLogContext._log != None:
            DistributedLogContext._log.__exit__(None, None, None)
            DistributedLogContext._log = None
