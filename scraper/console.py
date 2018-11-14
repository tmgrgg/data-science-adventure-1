from sqlalchemy.orm import sessionmaker
from builder import *

Session = sessionmaker(bind=engine)
session = Session()

def populate_db():
    session.add_all(industries)
    session.add_all(companies)
    session.add_all(jobs)
    session.add_all(cities)

populate_db()

# session.commit()
print(' <<<<<<<POPULATING DATABASE>>>>>>>>\n\n        ***DATABASE READY***\n\n*********YOU ARE AWESOME!!*********')
