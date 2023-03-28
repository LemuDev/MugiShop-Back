from src.config.db import db
from datetime import date


class Categories(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(60), unique=True)
    
    
    categories_rel = db.relationship("Products", backref="categories_rel")

class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(255))
    price = db.Column(db.Integer())
    image = db.Column(db.String(255))
    
    is_sell = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.Date(), default=date.today() )
    
    categories = db.Column(db.Integer, db.ForeignKey("categories.id"))
    
