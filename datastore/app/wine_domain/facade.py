import app.wine_domain.database as database
from app.wine_domain.distributed_log import DistributedLogContext
import app.api.circuit_breaker as circuit_breaker

#todo rename, does more than a facade should
def create(classified_wine):
    wine = database.create(classified_wine)
    try:
        log = DistributedLogContext.get_log()
        log.log_create(wine.id, classified_wine)
    except Exception as error:
        try:
            database.delete(wine.id)
        except Exception:
            circuit_breaker.wines_circuit_breaker.close(_distributed_log_message, 500)
        raise WineDomainError(_distributed_log_message) from error
    return wine.id

def retrieve(id):
    wine = database.retrieve(id)
    return wine

def delete(id):
    database.delete(id)
    try:
        log = DistributedLogContext.get_log()
        log.log_delete(id)
    except Exception as error:
        circuit_breaker.wines_circuit_breaker.close(_distributed_log_message, 500)
        raise WineDomainError(_distributed_log_message) from error

_distributed_log_message = 'Failed to propagate to the distributed log.'

class WineDomainError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
