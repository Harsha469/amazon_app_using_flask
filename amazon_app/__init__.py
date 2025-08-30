from flask import Flask
from config.config import Config
from flask_sqlalchemy import SQLAlchemy

#creating an instance of flask
app = Flask(__name__)

#telling to flask application use this configuration settings
app.config.from_object(Config)

#creating an instance of db and making connection to database is done
db = SQLAlchemy(app)



