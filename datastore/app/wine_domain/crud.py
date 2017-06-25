import app.wine_domain.model as model
from app.api.restplus import flask_app
import sys

def create(classified_wine, log):
    merged_wine = {**{'wine_class': classified_wine['wine_class']}, **classified_wine['wine']}
    wine = model.Wine(**merged_wine)
    session = model.Session()
    session.add(wine)
    session.commit()
    log.log_create(wine.id, classified_wine)
    return wine.id

def delete(id, log):
    session = model.Session()
    wine = session.query(model.Wine).filter_by(id=id).first()
    if wine is None:
        raise (UnknownRecordError(id))
    session.delete(wine)
    session.commit()
    log.log_delete(id)

def retrieve(id):
    session = model.Session()
    wine = session.query(model.Wine).filter_by(id=id).first()
    if wine is None:
        raise (UnknownRecordError(id))
    session.rollback()
    return wine

class UnknownRecordError(Exception):
    def __init__(self, id):
        self.message = "No record with id '{}' found.".format(id)
