from app.api.wines_endpoint import Wines
from nose.tools import assert_equals

def test_get_decorators():
    _assert_decorators(Wines.get, 'get')
    _assert_decorators(Wines.delete, 'delete')
    _assert_decorators(Wines.post, 'post')

def _assert_decorators(f, f_name):
    assert_equals(f.__name__, 'decorated_circuit_breaker_f')
    assert_equals(f.__wrapped__.__name__, 'error_handling_f')
    assert_equals(f.__wrapped__.__wrapped__.__name__, f_name)
