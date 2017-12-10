from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

engine = create_engine('sqlite:////tmp/test.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()

def initialize():
    Base.metadata.create_all(engine)

class Wine(Base):
    __tablename__ = 'Wines'
    id = Column(Integer, primary_key=True)
    wine_class = Column(String(1))
    alcohol = Column(Float())
    malic_acid = Column(Float())
    ash = Column(Float())
    alcalinity_of_ash = Column(Float())
    magnesium =  Column(Integer())
    total_phenols = Column(Float())
    flavanoids = Column(Float())
    nonflavanoid_phenols = Column(Float())
    proanthocyanins = Column(Float())
    color_intensity = Column(Float())
    hue = Column(Float())
    odxxx_of_diluted_wines = Column(Float())
    proline = Column(Integer())

def create(classified_wine, id = None):
    merged_wine = {**{'wine_class': classified_wine['wine_class']}, **classified_wine['wine']}
    with _session_scope() as session:
        wine = Wine(**merged_wine)
        if id is not None:
            wine.id = id
        session.add(wine)
        session.flush()
        id = wine.id
        session.commit()
        return id

def retrieve(id):
    with _session_scope() as session:
        wine = _get(id, session)
        session.rollback()
        return _create_classified_wine(wine)

def delete(id):
    with _session_scope() as session:
        wine = _get(id, session)
        session.delete(wine)
        session.commit()

def _get(id, session):
    wine = session.query(Wine).filter_by(id=id).first()
    if wine is None:
        raise (UnknownRecordError(id))
    return wine

def read_all():
    with _session_scope() as session:
        wines = session.query(Wine)
        classified_wines = [_create_classified_wine(wine) for wine in wines]
        session.rollback()
        return classified_wines

@contextmanager
def _session_scope():
    session = Session()
    try:
        yield session
    finally:
        session.close()

class UnknownRecordError(Exception):
    http_status_code = 404

    def __init__(self, id):
        self.message = "No record with id '{}' found.".format(id)

    def __str__(self):
        return self.message

def _create_classified_wine(wine):
    wine_dict = _to_wine_property_dict(wine)
    return {'wine_class': wine.wine_class, 'wine': wine_dict}

def _to_wine_property_dict(wine):
    return {
        'alcohol': wine.alcohol,
        'malic_acid': wine.malic_acid,
        'ash': wine.ash,
        'alcalinity_of_ash': wine.alcalinity_of_ash,
        'magnesium': wine.magnesium,
        'total_phenols': wine.total_phenols,
        'flavanoids': wine.flavanoids,
        'nonflavanoid_phenols': wine.nonflavanoid_phenols,
        'proanthocyanins': wine.proanthocyanins,
        'color_intensity': wine.color_intensity,
        'hue': wine.hue,
        'odxxx_of_diluted_wines': wine.odxxx_of_diluted_wines,
        'proline': wine.proline}
