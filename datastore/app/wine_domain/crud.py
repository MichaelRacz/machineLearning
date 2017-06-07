import app.wine_domain.model as model

def create(classified_wine):
    merged_wine = {**{'wine_class': classified_wine['wine_class']}, **classified_wine['wine']}
    wine = model.Wine(**merged_wine)
    session = model.Session()
    session.add(wine)
    session.commit()
    return wine.id

def delete(id):
    session = model.Session()
    wine = session.query(model.Wine).filter_by(id=id).first()
    if wine is None:
        raise (UnknownRecordError(id))
    session.delete(wine)
    session.commit()

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
