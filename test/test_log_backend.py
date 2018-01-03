from subprocess import run, PIPE, Popen
from pykafka import KafkaClient
from pykafka.common import OffsetType
import json

class TestLogBackend:
    """
    Enacapsulation of kafka test container management
    """
    def __init__(self, environment, hosts, topic_name):
        """
        Setup kafka containers and kafka client
        """
        if environment == 'DEV':
            process = self._execute(args = ['docker-compose',
                '--file', 'docker-compose.yml',
                '--file', 'docker-compose.dev.yml',
                'up', '-d'])
        self._environment = environment
        self._client = KafkaClient(hosts=hosts)
        self.hosts = hosts
        self.topic_name = topic_name

    def reset_topic(self):
        """
        Delete wine topic and create a new one with the same name
        """
        command = ("docker run --rm --net=host wurstmeister/kafka "
            "/bin/bash -c 'kafka-topics.sh --delete --topic {0} --zookeeper localhost:2181; "
            "if [ $? -eq 0 ]; then "
            "kafka-topics.sh --create --topic {0} --partitions 1 --replication-factor 1 --zookeeper localhost:2181; "
            "fi'"
            ).format(self.topic_name)
        print("RUNNING:" + command)
        run(command, shell=True)

    def create_consumer(self):
        """
        Create a consumer of the wine topic
        """
        topic = self._client.topics[self.topic_name.encode('ascii')]
        return topic.get_simple_consumer(consumer_timeout_ms=100,
            auto_offset_reset=OffsetType.EARLIEST,
            reset_offset_on_start=False)

    def create_producer(self):
        """
        Create a producer for the wine topic
        """
        topic = self._client.topics[self.topic_name.encode('ascii')]
        return topic.get_sync_producer()

    def tear_down(self):
        """
        Shutdown kafka containers
        """
        if self._environment == 'DEV':
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
