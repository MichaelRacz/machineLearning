import common.app.wine_db as wine_db
from app.wine_domain.distributed_log import DistributedLogContext

def create(classified_wine):
    id = _insert_into_db(classified_wine)
    try:
        log = DistributedLogContext.get_log()
        log.log_create(id, classified_wine)
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
    with wine_db.session_scope() as session:
        wine = _get(id, session)
        session.rollback()
        return wine_db.create_classified_wine(wine)

def delete(id):
    _delete_from_db(id)
    try:
        log = DistributedLogContext.get_log()
        log.log_delete(id)
    except Exception as error:
        # TODO: move closer to circuit breaker decoratee
        #circuit_breaker.wines_circuit_breaker.close(_distributed_log_message, 500)
        raise WineDomainError(_distributed_log_message, error) from error

_distributed_log_message = 'Failed to propagate to the distributed log.'

#TODO: rename
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
    with wine_db.session_scope() as session:
        wine = wine_db.Wine(**merged_wine)
        if id is not None:
            wine.id = id
        session.add(wine)
        session.flush()
        id = wine.id
        session.commit()
        return id

def _delete_from_db(id):
    with wine_db.session_scope() as session:
        wine = _get(id, session)
        session.delete(wine)
        session.commit()

def _get(id, session):
    wine = session.query(wine_db.Wine).filter_by(id=id).first()
    if wine is None:
        raise (UnknownRecordError(id))
    return wine

class UnknownRecordError(Exception):
    http_status_code = 404

    def __init__(self, id):
        self.message = "No record with id '{}' found.".format(id)

    def __str__(self):
        return self.message
