from dashpackage.__init__ import db

import pdb



class Job(db.Model):
    __tablename__ ="datasciencejobs"
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.TEXT)
    sal_upper = db.Column(db.Integer, nullable=True)
    sal_lower = db.Column(db.Integer, nullable=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'))
    industry_id = db.Column(db.TEXT, db.ForeignKey('industries.id'))
    glassdoorid = db.Column(db.Integer)
    salary_estimated = db.Column(db.Integer, nullable=True)
    listed_city = db.Column(db.TEXT)

    company = db.relationship('Company', back_populates ='jobs')
    city = db.relationship('City', back_populates='jobs')
    industry = db.relationship('Industry', back_populates='jobs')


class City(db.Model):
    __tablename__ = 'cities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT)
    expenses = None or db.Column(db.Integer)

    jobs = db.relationship('Job', back_populates='city')

class Company(db.Model):
    __tablename__ = 'companies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.TEXT)
    rating = db.Column(db.Integer)
    size_lower = db.Column(db.Integer)
    size_upper = db.Column(db.Integer)

    jobs= db.relationship('Job', back_populates='company')

class Industry(db.Model):
    __tablename__ = 'industries'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    jobs = db.relationship('Job', back_populates = 'industry')

db.create_all()

print('******Done with Models******')
