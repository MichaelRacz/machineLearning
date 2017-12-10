import app.wine_domain.database as database
from app.wine_domain.distributed_log import DistributedLogContext

def create(classified_wine):
    id = database.create(classified_wine)
    try:
        log = DistributedLogContext.get_log()
        log.log_create(id, classified_wine)
    except Exception as error:
        try:
            database.delete(id)
        except Exception:
            pass
            # TODO: move closer to circuit breaker decoratee
            # circuit_breaker.wines_circuit_breaker.close(_distributed_log_message, 500)
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
        # TODO: move closer to circuit breaker decoratee
        #circuit_breaker.wines_circuit_breaker.close(_distributed_log_message, 500)
        raise WineDomainError(_distributed_log_message, error) from error

_distributed_log_message = 'Failed to propagate to the distributed log.'

class WineDomainError(Exception):
    def __init__(self, message, inner_error=None):
        self.message = message
        self.inner_error = inner_error

    def __str__(self):
        return self.message

    def __repr__(self):
        inner_error_repr = repr(self.inner_error) if self.inner_error is not None else None
        return "WineDomainError ('{}'). Inner error: {}".format(self.message, inner_error_repr)
