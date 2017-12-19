from app.wine_domain.distributed_log import DistributedLogContext

# TODO: fix this dependency
import app.wine_domain.wines as database

from contextlib import contextmanager
from threading import Thread

@contextmanager
def synchronize_datastore():
    event_handler = EventHandler()
    thread = Thread(target=event_handler.handle)
    thread.start()
    yield None
    event_handler.stop()
    thread.join()

class EventHandler:
    def __init__(self):
        self._log = DistributedLogContext.get_log()

    def handle(self):
        for entry in self._log.read():
            if entry['type'] == 'create':
                database._insert_into_db(entry['classified_wine'], entry['id'])
            if entry['type'] == 'delete':
                database._delete_from_db(entry['id'])

    def stop(self):
        self._log.stop_read()
