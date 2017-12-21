from pykafka import KafkaClient
from app.api.restplus import flask_app
import json
from pykafka.common import OffsetType
from pykafka.exceptions import ConsumerStoppedException

class DistributedLog:
    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    def read(self):
        self._client = KafkaClient(hosts=flask_app.config['KAFKA_HOSTS'])
        self._topic = self._client.topics[flask_app.config['WINE_TOPIC'].encode('ascii')]
        self._consumer = self._topic.get_simple_consumer(
            auto_offset_reset=OffsetType.EARLIEST,
            reset_offset_on_start=True,
            consumer_timeout_ms=500)
        #TODO create config var or refactor
        for message in self._consumer:
            if message is not None:
                yield json.loads(message.value.decode('utf-8'))

    def stop_read(self):
        pass

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
