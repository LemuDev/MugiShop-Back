from flask import Flask
from src.config.db import db

from decouple import config
from os import getcwd


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config('SQLALCHEMY_DATABASE_URI')


db.init_app(app)




