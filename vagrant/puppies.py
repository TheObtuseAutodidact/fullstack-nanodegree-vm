import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Shelter(Base):
    __tablename__ = 'shelter'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(80))
    city = Column(String(80))
    state = Column(String(80))
    zipCode = Column(String(5))
    website = Column(String(80))


class Puppy(Base):
    __tablename__ = 'puppy'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    dateOfBirth = Column(Date)
    gender = Column(String(10))
    weight = Column(Numeric(10))
    picture = Column(String(250))
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)


### bottom
engine = create_engine('sqlite:///puppyshelter.db')

Base.metadata.create_all(engine)
