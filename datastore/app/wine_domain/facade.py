import app.wine_domain.database as database
from app.wine_domain.distributed_log import DistributedLogContext

def create(classified_wine):
    wine = database.create(classified_wine)
    log = DistributedLogContext.get_log()
    log.log_create(wine.id, classified_wine)
    return wine.id

def retrieve(id):
    wine = database.retrieve(id)
    return wine

def delete(id):
    database.delete(id)
    log = DistributedLogContext.get_log()
    log.log_delete(id)
