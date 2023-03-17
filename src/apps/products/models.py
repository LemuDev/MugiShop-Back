from src.config.db import db
from datetime import date




class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(60))
    description = db.Column(db.String(255))
    price = db.Column(db.Integer())
    image = db.Column(db.String(255))
    
    is_sell = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.Date(), default=date.today() )