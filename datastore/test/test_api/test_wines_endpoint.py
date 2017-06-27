from nose.tools import assert_equals, assert_true, assert_dict_equal
from testfixtures import LogCapture
from app.api.wines_endpoint import _handle_errors
from app.api.logger import logger
from app.wine_domain.crud import UnknownRecordError

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
