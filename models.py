# sql alchemy:
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, TEXT, Integer
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class DataScienceJob(Base):
    __tablename__ ="datasciencejobs"
    id = Column(Integer, primary_key = True)
    title = Column(TEXT)
    glassdoorid = Column(Integer)
    city_id = (Integer, ForeighKey('cities.id'))
    salary_level= Column(TEXT)
    city = relationship('City', back_populates='jobs')


class City(Base):
    __tablename__ = 'cities'
    id = Column(integer, primary_key=True)
    name = Column(TEXT)
    State_id = Column(TEXT)
    Income4comfortableliving = Column(Integer)
    jobs = relationship()


class Salary_range(Base):
    __tablename__ = 'salary_level'
    id = Column(Integer, primary_key=True)
    #leve= low, mid, high
    level = Column(TEXT)
    top = Column(Integer)
    bottom = Column(Integer)
    jobs= Relationship('DataScienceJob')

engine = sqlalchemy.create_engine('sqlite:///list.db', echo=True)
#links the defined class to the engine
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
