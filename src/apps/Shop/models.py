from src.config.db import db
from datetime import date

# Categories Model
class Categories(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(60), unique=True)
    
    
    categories_rel = db.relationship("Products", backref="categories_rel")

# Products Model
class Products(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(255))
    price = db.Column(db.Integer())
    image = db.Column(db.String(255))
    
    is_sell = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.Date(), default=date.today() )
    
    categories = db.Column(db.Integer, db.ForeignKey("categories.id"))
    
    cart = db.relationship('CartItems', backref='products')

# Cart Model
class Cart(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    cart_items = db.relationship('CartItems', backref='cart')
    
# Cart Items Model
class CartItems(db.Model):
    id = db.Column(db.Integer(), primary_key=True)    
    product_id = db.Column(db.Integer(), db.ForeignKey('products.id'))
    cart_id = db.Column(db.Integer(), db.ForeignKey('cart.id'))
    
        


        
    