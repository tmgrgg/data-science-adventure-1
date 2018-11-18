from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import dash

# creating flask server (which will hand queries through SQLALCHEMY)
server = Flask(__name__)
# add configurations and database
server.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///job_listings.db'
server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(server)


#initializing new dash app and connecting to flask server
app = dash.Dash(__name__, server=server,url_base_pathname='/dashboard/')


from dashpackage.dashboard import * 
