from flask import Flask
from flask_cors import CORS

from src.config.db import db
from src.config.ma import ma
from src.config.jwt import jwt

from decouple import config
from src.apps.Shop.router import bp as shop_router
from src.apps.Auth.router import bp as auth_router
from os import getcwd


# Create instance flask
app = Flask(__name__)

# Config From .Env variables
app.config["SQLALCHEMY_DATABASE_URI"] = config('SQLALCHEMY_DATABASE_URI')
app.config["SECRET_KEY"] = config("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = config('JWT_SECRET_KEY')

# Cors config for to allow access the front 
cors = CORS(
    app, 
    origins=['http://localhost:5173', 'http://127.0.0.1:5173']
)

# Register Modules Blueprints
app.register_blueprint(shop_router)
app.register_blueprint(auth_router)


# init All apps config
db.init_app(app)
ma.init_app(app)
jwt.init_app(app)






