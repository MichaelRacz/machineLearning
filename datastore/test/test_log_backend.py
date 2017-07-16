from app.api.restplus import flask_app
from subprocess import run, PIPE, Popen
from pykafka import KafkaClient
from pykafka.common import OffsetType
import json

class TestLogBackend:
    """
    Enacapsulation of kafka test container management
    """
    def initialize(self):
        """
        Setup kafka containers and kafka client
        """
        if flask_app.config['ENVIRONMENT'] == 'DEV':
            process = self._execute(args = ['docker-compose',
                '--file', 'docker-compose.yml',
                '--file', 'docker-compose.dev.yml',
                'up', '-d'])
        self._client = KafkaClient(hosts=flask_app.config['KAFKA_HOSTS'])

    def reset_topic(self):
        """
        Delete wine topic and create a new one with the same name
        """
        command = ("docker run --rm --net=host wurstmeister/kafka "
            "/bin/bash -c 'kafka-topics.sh --delete --topic {0} --zookeeper localhost:2181; "
            "if [ $? -eq 0 ]; then "
            "kafka-topics.sh --create --topic {0} --partitions 1 --replication-factor 1 --zookeeper localhost:2181; "
            "fi'"
            ).format(flask_app.config['WINE_TOPIC'])
        print("RUNNING:" + command)
        run(command, shell=True)

    def create_consumer(self):
        """
        Create a consumer of the wine topic
        """
        topic = self._client.topics[flask_app.config['WINE_TOPIC'].encode('ascii')]
        return topic.get_simple_consumer(consumer_timeout_ms=100,
            auto_offset_reset=OffsetType.EARLIEST,
            reset_offset_on_start=False)

    def create_producer(self):
        """
        Create a producer for the wine topic
        """
        topic = self._client.topics[flask_app.config['WINE_TOPIC'].encode('ascii')]
        return topic.get_sync_producer()

    def tear_down(self):
        """
        Shutdown kafka containers
        """
        if flask_app.config['ENVIRONMENT'] == 'DEV':
            shutdown_command = 'docker-compose --file docker-compose.yml --file docker-compose.dev.yml down'
            self._execute_in_new_process(shutdown_command)

    def _execute(self, args):
        """
        Run shell command in same process (current thread)
        """
        process = run(
            args = args,
            universal_newlines = True)
        if(process.returncode != 0):
            raise Exception('An error occurred while orchestrating the kafka ' \
                'test log backend. A stale docker container could be running. ' \
                'Detailed message: {}'.format(process.stdout))
        return process

    def _execute_in_new_process(self, command):
        """
        Run a shell command in another process (usually to avoid blocking the
        current process and 'gain' performance).
        """
        print('Running command: {}'.format(command))
        Popen(command, shell=True)
