from app.api.svc_classification_endpoint import SVC, svc_circuit_breaker
from test.test_api.common import assert_endpoint_decorators
from nose.tools import assert_equals

def test_decorators():
    assert_endpoint_decorators(SVC.post, 'post')

def test_circuit_breaker():
    assert_equals(svc_circuit_breaker._max_requests, 20)