from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

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
    wine = Wine(**merged_wine)
    if id is not None:
        wine.id = id
    session = Session()
    session.add(wine)
    session.commit()
    return wine

def retrieve(id):
    session = Session()
    wine = _get(id, session)
    session.rollback()
    return wine

def delete(id):
    session = Session()
    wine = _get(id, session)
    session.delete(wine)
    session.commit()

def _get(id, session):
    wine = session.query(Wine).filter_by(id=id).first()
    if wine is None:
        raise (UnknownRecordError(id))
    return wine

class UnknownRecordError(Exception):
    def __init__(self, id):
        self.message = "No record with id '{}' found.".format(id)

    def __str__(self):
        return self.message
