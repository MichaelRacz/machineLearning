from nose.tools import assert_equals, assert_true, assert_dict_equal
from testfixtures import LogCapture
from app.api.wines_endpoint import _handle_errors, CircuitBreaker
from app.api.logger import logger
from app.wine_domain.crud import UnknownRecordError
from time import sleep
from threading import Thread

def test_handle_errors():
    with LogCapture() as log:
        result = _handle_errors('foo')(decoratee)('x', y = 'z')
        assert_equals(result, 'expected result')
    assert_equals(log.records[0].levelname, 'INFO')
    assert_true("begin call 'foo', request id:" in log.records[0].msg)
    assert_equals(log.records[1].levelname, 'INFO')
    assert_equals(log.records[1].msg, 'method execution')
    assert_equals(log.records[2].levelname, 'INFO')
    assert_equals(log.records[2].msg, 'args x')
    assert_equals(log.records[3].levelname, 'INFO')
    assert_equals(log.records[3].msg, 'kwargs y = z')
    assert_equals(log.records[4].levelname, 'INFO')
    assert_true("end call 'foo', request id:" in log.records[4].msg)

def decoratee(*args, **kwargs):
    logger.info('method execution')
    logger.info('args {}'.format(str(*args)))
    for key in kwargs:
        logger.info('kwargs {} = {}'.format(key, kwargs[key]))
    return 'expected result'

def test_handle_errors_decoratee_raises_UnknownRecordError():
    with LogCapture() as log:
        result, status_code = _handle_errors('foo')(_raising_UnknownRecordError)()
        assert_dict_equal(result, {'error_message': "No record with id 'error message' found."})
        assert_equals(status_code, 404)
    _assert_failed_call(log)

def _raising_UnknownRecordError():
    raise UnknownRecordError('error message')

def test_handle_errors_decoratee_raises():
    with LogCapture() as log:
        result, status_code = _handle_errors('foo')(_raising_Exception)()
        assert_dict_equal(result, {'error_message': 'error message'})
        assert_equals(status_code, 500)
    _assert_failed_call(log)

def _raising_Exception():
    raise Exception('error message')

def _assert_failed_call(log):
    assert_equals(log.records[0].levelname, 'INFO')
    assert_true("begin call 'foo', request id:" in log.records[0].msg)
    assert_equals(log.records[1].levelname, 'ERROR')
    assert_true("failed call 'foo', request id:" in log.records[1].msg)

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
