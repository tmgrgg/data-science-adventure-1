# sql alchemy:
from sqlalchemy import*
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import pdb

Base = declarative_base()

class Job(Base):
    __tablename__ ="datasciencejobs"
    id = Column(Integer, primary_key = True)
    title = Column(TEXT)
    sal_upper = Column(Integer, nullable=True)
    sal_lower = Column(Integer, nullable=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    city_id = Column(Integer, ForeignKey('cities.id'))
    industry_id = Column(TEXT, ForeignKey('industries.id'))
    glassdoorid = Column(Integer)
    salary_estimated = Column(Integer, nullable=True)
    listed_city = Column(TEXT)
    # comp_name = Column(TEXT)#to be used in company setter function
    # ind_name = Column(TEXT)#to be used industry setter function only
    # cit_name = Column(TEXT)#to be used city setter function only

    company = relationship('Company', back_populates ='jobs')
    city = relationship('City', back_populates='jobs')
    industry = relationship('Industry', back_populates='jobs')


class City(Base):
    __tablename__ = 'cities'
    id = Column(Integer, primary_key=True)
    name = Column(TEXT)
    expenses = None or Column(Integer)

    jobs = relationship('Job', back_populates='city')

class Company(Base):
    __tablename__ = 'companies'
    id = Column(Integer, primary_key=True)
    name = Column(TEXT)
    rating = Column(Integer)
    size_lower = Column(Integer)
    size_upper = Column(Integer)

    jobs= relationship('Job', back_populates='company')

class Industry(Base):
    __tablename__ = 'industries'
    id = Column(Integer, primary_key=True)
    name = Column(Text)

    jobs = relationship('Job', back_populates = 'industry')



engine = create_engine('sqlite:///job_listings.db', echo=True)

#links the defined class to the engine
Base.metadata.create_all(engine)

print('<<<<<<<DONE CREATING SCHEMA>>>>>>>>')
