from app.api.circuit_breaker import CircuitBreaker
from time import sleep
from threading import Thread
from nose.tools import assert_equals, assert_dict_equal

class TestCircuitBreaker:
    def setup(self):
        self.circuit_breaker = CircuitBreaker(2)

    def test_close(self):
        self.circuit_breaker.close('reason', 1337)
        result, status_code = self.circuit_breaker.decorate(lambda: 'dummy')()
        assert_equals(status_code, 1337)
        assert_dict_equal(result, {'error_message': 'reason'})

    def test_decorate(self):
        def decoratee(x, y = 'dummy'):
            assert_equals(x, 'x')
            assert_equals(y, 'z')
            return 'result'
        result = self.circuit_breaker.decorate(decoratee)('x', y = 'z')
        assert_equals(result, 'result')

    def test_decorate_too_many_requests(self):
        wait = True
        def decoratee():
            while wait:
                sleep(0.1)
        thread1 = Thread(target=self.circuit_breaker.decorate(decoratee))
        thread2 = Thread(target=self.circuit_breaker.decorate(decoratee))
        try:
            thread1.start()
            thread2.start()
            result, status_code = self.circuit_breaker.decorate(lambda: 'dummy')()
            assert_equals(status_code, 429)
            assert_dict_equal(result, {'error_message': 'Too many requests.'})
        finally:
            wait = False
            thread1.join(0.2)
            thread2.join(0.2)
        result = self.circuit_breaker.decorate(lambda: 'request count is decreased')()
        assert_equals(result, 'request count is decreased')
