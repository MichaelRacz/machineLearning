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

@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
    finally:
        session.close()

#TODO: Move somewhere else?
def create_classified_wine(wine):
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
