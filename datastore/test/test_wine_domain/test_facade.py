import app.wine_domain.facade as facade
import app.wine_domain.database as database
import app.api.circuit_breaker as circuit_breaker
from app.wine_domain.distributed_log import DistributedLogContext
from nose.tools import assert_equals, assert_true, assert_is
from collections import namedtuple

def test_create_lets_database_errors_pass_through():
    initial_create = database.create
    error = Exception('message')
    def create(dummy):
        raise error
    database.create = create
    try:
        caught_error = None
        try:
            facade.create('dummy')
        except Exception as database_error:
            caught_error = database_error
        assert_is(caught_error, error)
    finally:
        database.create = initial_create

def test_create_deletes_when_distributed_log_throws():
    initial_create = database.create
    database.create = lambda x: namedtuple('Stub', 'id')('1234')
    initial_log = DistributedLogContext._log
    create_error = Exception('message')
    DistributedLogContext._log = _LogStub(create_error)
    initial_delete = database.delete
    deleted = False
    def delete(id):
        assert_equals(id, '1234')
        nonlocal deleted
        deleted = True
    database.delete = delete
    try:
        error = None
        try:
            facade.create('dummy')
        except facade.WineDomainError as domain_error:
            error = domain_error
        assert_equals(error.message, 'Failed to propagate to the distributed log.')
        assert_true(deleted)
    finally:
        database.create = initial_create
        DistributedLogContext._log = initial_log
        database.delete = initial_delete

def test_create_closes_circuit_breaker_when_compensation_fails():
    initial_create = database.create
    database.create = lambda x: namedtuple('Stub', 'id')('1234')
    initial_log = DistributedLogContext._log
    create_error = Exception('dummy')
    DistributedLogContext._log = _LogStub(create_error)
    initial_delete = database.delete
    delete_error = Exception('dummy')
    def delete(id):
        raise delete_error
    database.delete = delete
    initial_circuit_breaker = circuit_breaker.wines_circuit_breaker
    circuit_breaker.wines_circuit_breaker = _CircuitBreakerStub('Failed to propagate to the distributed log.', 500)
    try:
        error = None
        try:
            facade.create('dummy')
        except facade.WineDomainError as domain_error:
            error = domain_error
        assert_equals(error.message, 'Failed to propagate to the distributed log.')
        assert_true(api.circuit_breaker.is_closed)
    finally:
        database.create = initial_create
        DistributedLogContext._log = initial_log
        database.delete = initial_delete
        circuit_breaker.wines_circuit_breaker = initial_cuircuit_breaker

class _LogStub:
    def __init__(self, error):
        self.error = error

    def log_create(self, id, classified_wine):
        raise self.error

class _CircuitBreakerStub:
    def __init__(self, expected_reason, expected_status_code):
        self.expected_reason = expected_reason
        self.expected_status_code = expected_status_code
        self.is_closed = False

    def close(self, reason, status_code):
        assert_equlals(reason, self.expected_reason)
        assert_equlals(status_code, self.expected_status_code)
        self.is_closed = True