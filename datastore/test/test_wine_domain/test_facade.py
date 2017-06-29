import app.wine_domain.facade as facade
import app.wine_domain.database as database
from app.wine_domain.distributed_log import DistributedLogContext
from nose.tools import assert_equals, assert_true, assert_is
from collections import namedtuple

def test_create_deletes_when_distributed_log_throws():
    initial_create = database.create
    database.create = lambda x: namedtuple('Stub', 'id')('1234')
    initial_log = DistributedLogContext._log
    create_error = Exception('message')
    class LogStub:
        def log_create(self, id, classified_wine):
            raise create_error
    DistributedLogContext._log = LogStub()
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
