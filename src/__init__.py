from flask import Flask
from flask_cors import CORS

from src.config.db import db
from src.config.ma import ma
from src.config.jwt import jwt

from decouple import config

# Blueprints modules importatation
from src.apps.modules.cart.router import bp as cart_bp
from src.apps.modules.categories.router import bp as categories_bp
from src.apps.modules.product_sell.router import bp as product_sell_bp
from src.apps.modules.products.router import bp as products_bp
from src.apps.modules.users.router import bp as user_bp


# Models importation
from src.apps.modules.cart.model import *
from src.apps.modules.categories.model import *
from src.apps.modules.products.model import *
from src.apps.modules.users.model import *



# Create instance flask
app = Flask(__name__)

# Config From .Env variables
app.config["SQLALCHEMY_DATABASE_URI"] = config('SQLALCHEMY_DATABASE_URI')
app.config["SECRET_KEY"] = config("SECRET_KEY")
app.config["JWT_SECRET_KEY"] = config('JWT_SECRET_KEY')

# Cors config for to allow access the front 
cors = CORS(
    app, 
    origins=['http://localhost:5000', 'http://127.0.0.1:5000']
)

# Register Modules Blueprints
app.register_blueprint(categories_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(user_bp)
app.register_blueprint(products_bp)
app.register_blueprint(product_sell_bp)


# init All apps config
db.init_app(app)
ma.init_app(app)
jwt.init_app(app)





def db_init():
    with app.app_context():
        db.drop_all()
        db.create_all()