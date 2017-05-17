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
