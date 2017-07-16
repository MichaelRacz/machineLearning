import app.wine_domain.database as database
from app.wine_domain.distributed_log import DistributedLogContext
import app.api.wines_endpoint as wines_endpoint

def create(classified_wine):
    id = database.create(classified_wine)
    try:
        log = DistributedLogContext.get_log()
        log.log_create(id, classified_wine)
    except Exception as error:
        try:
            database.delete(wine.id)
        except Exception:
            wines_endpoint.wines_circuit_breaker.close(_distributed_log_message, 500)
        raise WineDomainError(_distributed_log_message, error) from error
    return id

def retrieve(id):
    classified_wine = database.retrieve(id)
    return classified_wine

def delete(id):
    database.delete(id)
    try:
        log = DistributedLogContext.get_log()
        log.log_delete(id)
    except Exception as error:
        wines_endpoint.wines_circuit_breaker.close(_distributed_log_message, 500)
        raise WineDomainError(_distributed_log_message, error) from error

_distributed_log_message = 'Failed to propagate to the distributed log.'

class WineDomainError(Exception):
    def __init__(self, message, inner_error=None):
        self._message = message
        self._inner_error = inner_error

    def __str__(self):
        return self._message

    def __repr__(self):
        inner_error_repr = repr(self._inner_error) if self._inner_error is not None else None
        return "WineDomainError ('{}'). Inner error: {}".format(self._message, inner_error_repr)
