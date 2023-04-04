from flask import Flask
from src.config.db import db
from src.config.ma import ma
from decouple import config
from src.apps.Shop.router import bp as shop_router
from src.apps.Auth.router import bp as auth_router
from os import getcwd



app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = config('SQLALCHEMY_DATABASE_URI')

app.register_blueprint(shop_router)
app.register_blueprint(auth_router)



db.init_app(app)
ma.init_app(app)







