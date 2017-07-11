from app.api.restplus import flask_app
from subprocess import run, PIPE, Popen
#from kafka import KafkaConsumer
from pykafka import KafkaClient
from pykafka.common import OffsetType
import json

class TestLogBackend:
    def initialize(self):
        if flask_app.config['ENVIRONMENT'] == 'DEV':
            process = self._execute(args = ['docker-compose',
                '--file', 'docker-compose.yml',
                '--file', 'docker-compose.dev.yml',
                'up', '-d'])
        self._client = KafkaClient(hosts=flask_app.config['KAFKA_HOSTS'])
        #process = self._execute(
        #    args = ['docker', 'run',
        #        '-d',
        #        '--name', 'kafka_test_instance',
        #        '--env', 'ADVERTISED_HOST=0.0.0.0',
        #        '--env', 'ADVERTISED_PORT=9092',
        #        '--env', 'LISTENERS=0.0.0.0:9092',
        #        '--env', 'ADVERTISED_LISTENERS=0.0.0.0:9092',
        #        '--env', 'TOPICS={}'.format(flask_app.config['WINE_TOPIC']),
        #        'spotify/kafka'])
        #self.container_hash = process.stdout.rstrip()
        #process = self._execute(
        #    args = ['docker', 'inspect',
        #        '--format', '{{.NetworkSettings.IPAddress}}',
        #        self.container_hash])
        #container_ip = process.stdout.rstrip()
        #self.kafka_socket = '{}:9092'.format(container_ip)
        #flask_app.config['KAFKA_BROKER'] = self.kafka_socket

    def reset_topic(self):
        command = ("docker run --rm --net=host wurstmeister/kafka "
            "/bin/bash -c 'kafka-topics.sh --delete --topic {0} --zookeeper localhost:2181; "
            "if [ $? -eq 0 ]; then "
            "kafka-topics.sh --create --topic {0} --partitions 1 --replication-factor 1 --zookeeper localhost:2181; "
            "fi'"
            ).format(flask_app.config['WINE_TOPIC'])
        print("RUNNING:" + command)
        run(command, shell=True)

    def create_consumer(self):
        topic = self._client.topics[flask_app.config['WINE_TOPIC'].encode('ascii')]
        # Move to config?
        return topic.get_simple_consumer(consumer_timeout_ms=100,
            auto_offset_reset=OffsetType.EARLIEST,
            reset_offset_on_start=False)
        #return KafkaConsumer(flask_app.config['WINE_TOPIC'],
        #    bootstrap_servers=[self.kafka_socket],
        #    #api_version=(0,8,0),
        #    key_deserializer=lambda m: m.decode('utf-8'),
        #    value_deserializer=lambda m: json.loads(m.decode('utf-8')))

    def create_producer(self):
        topic = self._client.topics[flask_app.config['WINE_TOPIC'].encode('ascii')]
        return topic.get_sync_producer()

    def tear_down(self):
        #process = self._execute(args = ['docker-compose',
        #    '--file', 'docker-compose.dev.yml',
        #    'down'])
        if flask_app.config['ENVIRONMENT'] == 'DEV':
            shutdown_command = 'docker-compose --file docker-compose.yml --file docker-compose.dev.yml down'
            self._execute_in_new_process(shutdown_command)

    def _execute(self, args):
        process = run(
            args = args,
            universal_newlines = True)#,
            #stdout=PIPE,
            #stderr=PIPE)
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
        Popen(command, shell=True) #, stdout=PIPE, stderr=PIPE)
