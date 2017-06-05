import app.db_model as db_model

def create(classified_wine):
    merged_wine = {**{'wine_class': classified_wine['wine_class']}, **classified_wine['wine']}
    wine = db_model.Wine(**merged_wine)
    session = db_model.Session()
    session.add(wine)
    session.commit()
    return wine.id

def delete(id):
    session = db_model.Session()
    wine = session.query(db_model.Wine).filter_by(id=id).first()
    if(wine is None):
        raise (UnknownRecordError(id))
    session.delete(wine)
    session.commit()

def retrieve(id):
    session = db_model.Session()
    wine = session.query(db_model.Wine).filter_by(id=id).first()
    if(wine is None):
        raise (UnknownRecordError(id))
    session.rollback()
    return wine

class UnknownRecordError(Exception):
    def __init__(self, id):
        self.message = "No record with id '{}' found.".format(id)
