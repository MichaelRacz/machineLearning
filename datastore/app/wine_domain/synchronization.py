from app.wine_domain.distributed_log import DistributedLogContext
import app.wine_domain.database as database

def synchronize_datastore():
    log = DistributedLogContext.get_log()
    for entry in log.read():
        if entry['type'] == 'create':
            database.create(entry['classified_wine'], entry['id'])
        if entry['type'] == 'delete':
            database.delete(entry['id'])
