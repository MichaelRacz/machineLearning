from app.api.wines_endpoint import Wines
from app.api.circuit_breaker import wines_circuit_breaker
from test.test_api.common import assert_endpoint_decorators
from nose.tools import assert_equals

def test_decorators():
    assert_endpoint_decorators(Wines.get, 'get')
    assert_endpoint_decorators(Wines.delete, 'delete')
    assert_endpoint_decorators(Wines.post, 'post')

def test_circuit_breaker():
    assert_equals(wines_circuit_breaker._max_requests, 20)
