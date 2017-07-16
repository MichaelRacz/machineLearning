from app.api.nearest_neighbor_classification_endpoint import NearestNeighbor, nearest_neighbor_circuit_breaker
from test.test_api.common import assert_endpoint_decorators
from nose.tools import assert_equals

def test_decorators():
    assert_endpoint_decorators(NearestNeighbor.post, 'post')

def test_circuit_breaker():
    assert_equals(nearest_neighbor_circuit_breaker._max_requests, 20)
