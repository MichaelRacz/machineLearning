from app.api.restplus import flask_app
from subprocess import run, PIPE

class TestLogBackend:
    def initialize(self):
        process = self._execute(
            args = ['docker', 'run',
                '-d',
                '--env', 'TOPICS={}'.format(flask_app.config['WINE_TOPIC']),
                '--name', 'kafka_test_instance',
                'spotify/kafka'])
        self.container_hash = process.stdout.rstrip()
        process = self._execute(
            args = ['docker', 'inspect',
                '--format', '{{.NetworkSettings.IPAddress}}',
                self.container_hash])
        container_ip = process.stdout
        kafka_socket = '{}:9032'.format(container_ip)

    def tear_down(self):
        self._execute(args = ['docker', 'stop', self.container_hash])
        self._execute(args = ['docker', 'rm', self.container_hash])

    def _execute(self, args):
        process = run(
            args = args,
            universal_newlines = True,
            stdout=PIPE,
            stderr=PIPE)
        if(process.returncode != 0):
            raise Exception('An error occurred while orchestrating the kafka ' \
                'test log backend. A stale docker container could be running. ' \
                'Detailed message: {}'.format(process.stdout))
        return process
