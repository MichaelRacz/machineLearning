import app.wine_domain.database as database
from app.wine_domain.distributed_log import DistributedLogContext

def create(classified_wine):
    wine = database.create(classified_wine)
    try:
        log = DistributedLogContext.get_log()
        log.log_create(wine.id, classified_wine)
    except Exception as error:
        database.delete(wine.id)
        raise WineDomainError('Failed to propagate to the distributed log.') from error
    return wine.id

def retrieve(id):
    wine = database.retrieve(id)
    return wine

def delete(id):
    database.delete(id)
    log = DistributedLogContext.get_log()
    log.log_delete(id)

class WineDomainError(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message
