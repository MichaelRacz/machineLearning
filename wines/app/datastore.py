from pykafka import KafkaClient
import json
from wines.app import database

producer = None

def init(kafka_hosts, topic_name):
    client = KafkaClient(hosts=kafka_hosts)
    topic = client.topics[topic_name.encode('ascii')]
    global producer
    producer = topic.get_sync_producer()

def exit():
    global producer
    if producer is not None:
        producer.__exit__(None, None, None)
        producer = None

def create(classified_wine):
    id = _insert_into_db(classified_wine)
    try:
        _log_create(id, classified_wine)
    except Exception as error:
        try:
            _delete_from_db(id)
        except Exception:
            pass
            # TODO: move closer to circuit breaker decoratee
            # circuit_breaker.wines_circuit_breaker.close(_distributed_log_message, 500)
        raise WineDomainError(_distributed_log_message, error) from error
    return id

def retrieve(id):
    with database.session_scope() as session:
        wine = _get(id, session)
        session.rollback()
        return database.create_classified_wine(wine)

def delete(id):
    _delete_from_db(id)
    try:
        _log_delete(id)
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

def _insert_into_db(classified_wine, id = None):
    merged_wine = {**{'wine_class': classified_wine['wine_class']}, **classified_wine['wine']}
    with database.session_scope() as session:
        wine = database.Wine(**merged_wine)
        if id is not None:
            wine.id = id
        session.add(wine)
        session.flush()
        id = wine.id
        session.commit()
        return id

def _delete_from_db(id):
    with database.session_scope() as session:
        wine = _get(id, session)
        session.delete(wine)
        session.commit()

def _get(id, session):
    wine = session.query(database.Wine).filter_by(id=id).first()
    if wine is None:
        raise (UnknownRecordError(id))
    return wine

class UnknownRecordError(Exception):
    http_status_code = 404

    def __init__(self, id):
        self.message = "No record with id '{}' found.".format(id)

    def __str__(self):
        return self.message

def _log_create(id, classified_wine):
    event = {
        'type': 'create',
        'version': '1',
        'id': id,
        'classified_wine': classified_wine
    }
    producer.produce(json.dumps(event).encode('utf-8'))

def _log_delete(id):
    event = {
        'type': 'delete',
        'version': '1',
        'id': id
    }
    producer.produce(json.dumps(event).encode('utf-8'))
