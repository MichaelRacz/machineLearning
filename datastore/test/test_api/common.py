from nose.tools import assert_equals

def assert_endpoint_decorators(f, f_name):
    assert_equals(f.__name__, 'decorated_circuit_breaker_f')
    assert_equals(f.__wrapped__.__name__, 'error_handling_f')
    assert_equals(f.__wrapped__.__wrapped__.__name__, f_name)
