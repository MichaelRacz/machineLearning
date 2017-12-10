from nose.tools import assert_equals, assert_true, assert_dict_equal, assert_is, assert_in
from testfixtures import LogCapture
from common.app.error_handler import handle_errors
from common.app.logger import logger
from werkzeug.exceptions import HTTPException

def test_handle_errors():
    def decoratee(*args, **kwargs):
        logger.info('method execution')
        logger.info('args {}'.format(str(*args)))
        for key in kwargs:
            logger.info('kwargs {} = {}'.format(key, kwargs[key]))
        return 'expected result'
    with LogCapture() as log:
        result = handle_errors('foo')(decoratee)('x', y = 'z')
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

def test_handle_errors_reraises_HTTPException():
    http_exception = HTTPException()
    def decoratee():
        raise http_exception
    with LogCapture() as log:
        try:
            handle_errors('foo')(decoratee)()
            assert_true(False, 'exception should be re-raised')
        except Exception as error:
            assert_is(error, http_exception)
    assert_equals(log.records[0].levelname, 'INFO')
    assert_true("begin call 'foo', request id:" in log.records[0].msg)
    assert_equals(log.records[1].levelname, 'ERROR')
    assert_true("failed call 'foo' (framework validation), request id:" in log.records[1].msg)

def test_handle_errors_decoratee_raises_error_with_http_status_code():
    def decoratee():
        error = Exception('error message')
        error.http_status_code = 444
        raise error
    with LogCapture() as log:
        result, status_code = handle_errors('foo')(decoratee)()
        assert_dict_equal(result, {'error_message': 'error message'})
        assert_equals(status_code, 444)
    _assert_failed_call(log)

def test_handle_errors_decoratee_raises():
    def decoratee():
        raise Exception('error message')
    with LogCapture() as log:
        result, status_code = handle_errors('foo')(decoratee)()
        assert_dict_equal(result, {'error_message': 'error message'})
        assert_equals(status_code, 500)
    _assert_failed_call(log)

def _assert_failed_call(log):
    assert_equals(log.records[0].levelname, 'INFO')
    assert_true("begin call 'foo', request id:" in log.records[0].msg)
    assert_equals(log.records[1].levelname, 'ERROR')
    assert_true("failed call 'foo', request id:" in log.records[1].msg)
